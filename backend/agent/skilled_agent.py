"""SkilledAgent – a Pydantic AI Agent subclass with a sandboxed filesystem
and agent skills support.

Usage (auto-created temp directory):
    from agent import SkilledAgent
    from pathlib import Path

    agent = SkilledAgent(
        model='anthropic:claude-3-5-sonnet-latest',
        skills=[Path("my-skills/organize-notes")],
        instructions="You are a meticulous research assistant.",
    )

    # Access the auto-created work directory
    print(f"Workspace: {agent.work_dir}")

    # Write files using pathlib
    (agent.work_dir / "notes.txt").write_text("hello world")
    result = agent.run_sync("Count the words in /notes.txt.")

    # Cleanup explicitly (or let __del__ handle it)
    agent.cleanup()

Usage (explicit work_dir):
    import tempfile
    from pathlib import Path

    with tempfile.TemporaryDirectory() as tmp:
        agent = SkilledAgent(
            model='anthropic:claude-3-5-sonnet-latest',
            work_dir=tmp,
            skills=[Path("my-skills/organize-notes")],
            instructions="You are a meticulous research assistant.",
        )

        Path(tmp, "notes.txt").write_text("hello world foo bar")
        result = agent.run_sync("Count the words in /notes.txt.")
        print(result.output)
"""

import atexit
import shutil
import tempfile
import weakref
from pathlib import Path
from typing import Any

from pydantic_ai import Agent
from pydantic_ai_filesystem_sandbox import FileSystemToolset, Sandbox, SandboxConfig, Mount
from pydantic_ai_skills import SkillsCapability


# Skills are always stored under this path inside the sandbox work_dir
_SKILLS_SUBDIR = Path(".agent") / "skills"
_SKILL_REFERENCES_TEMPLATE_SUBDIR = Path("references") / "template"
_REPO_ROOT = Path(__file__).resolve().parents[2]
_TEMPLATES_SOURCE_DIR = _REPO_ROOT / "templates"

_FILESYSTEM_INSTRUCTIONS = (
    "You have access to a sandboxed filesystem. "
    "Virtual root '/' maps to a temporary working directory on the host. "
    "All paths must start with '/'. "
    "Use the file tools to read, write, edit, copy, move, delete, and list files; "
    "parent directories are created automatically when writing. "
    "Be precise about filenames and paths. Report clearly what you did."
)

_DEFAULT_PERSONALITY = "You are a helpful assistant with access to a sandboxed filesystem."


# ---------------------------------------------------------------------------
# Weak reference registry for auto-created temp directories.
# atexit ensures cleanup even if __del__ doesn't run before interpreter exit.
# ---------------------------------------------------------------------------
_TEMP_DIR_AGENTS: weakref.WeakValueDictionary[int, "SkilledAgent"] = (
    weakref.WeakValueDictionary()
)


def _cleanup_all_temp_dirs() -> None:
    """atexit handler: clean up any surviving auto-created temp directories."""
    for agent in list(_TEMP_DIR_AGENTS.values()):
        try:
            agent.cleanup()
        except Exception:
            pass


atexit.register(_cleanup_all_temp_dirs)


class SkilledAgent(Agent):
    """A Pydantic AI Agent pre-configured with a sandboxed filesystem and
    optional agent skills.

    All standard Agent constructor parameters are supported and passed through
    transparently. The sandbox toolset and skills capability are merged with
    any caller-provided toolsets/capabilities.

    Skills are always stored under <work_dir>/.agent/skills/ inside the sandbox.
    When skill paths are supplied they are copied into that directory, preserving
    each skill directory's name.

    If no instructions are provided a default personality is used. If
    instructions are provided, the filesystem (and skills) operational
    instructions are appended without altering the caller's stated personality
    or purpose.

    Args:
        work_dir: Host directory mounted as virtual root "/" inside the sandbox.
                  If not provided, a temporary directory is created automatically
                  and will be cleaned up when the agent is garbage collected or
                  when cleanup() is called explicitly.
        skills: Optional list of paths to skill directories (each containing a
                SKILL.md). Each directory is copied into <work_dir>/.agent/skills/
                under its own name.
        **kwargs: Any keyword arguments accepted by pydantic_ai.Agent.
    """

    def __init__(
        self,
        model: Any,
        *,
        work_dir: str | Path | None = None,
        skills: list[str | Path] | None = None,
        **kwargs: Any,
    ) -> None:
        # ------------------------------------------------------------------
        # Resolve work_dir – create a temp directory if none provided
        # ------------------------------------------------------------------
        if work_dir is None:
            self._work_dir = Path(tempfile.mkdtemp(prefix="skilled-agent-"))
            self._owns_work_dir = True
            _TEMP_DIR_AGENTS[id(self)] = self
        else:
            self._work_dir = Path(work_dir)
            self._owns_work_dir = False

        # ------------------------------------------------------------------
        # Copy supplied skills into the sandbox's fixed skills directory
        # ------------------------------------------------------------------
        skills_dest = self._work_dir / _SKILLS_SUBDIR
        if skills:
            skills_dest.mkdir(parents=True, exist_ok=True)
            for src in skills:
                src = Path(src)
                shutil.copytree(src, skills_dest / src.name, dirs_exist_ok=True)

            # Make shared correspondence templates available inside each skill's
            # references directory for skills to reference consistently.
            #
            # NOTE: We intentionally fail fast when the source templates
            # directory is missing, because the screening agent relies on these
            # templates for candidate-facing correspondence generation.
            templates_src = _TEMPLATES_SOURCE_DIR
            if not templates_src.exists() or not templates_src.is_dir():
                raise FileNotFoundError(
                    f"Required templates directory not found: {templates_src}"
                )

            shared_templates_dest = self._work_dir / _SKILLS_SUBDIR / _SKILL_REFERENCES_TEMPLATE_SUBDIR
            shared_templates_dest.mkdir(parents=True, exist_ok=True)
            shutil.copytree(templates_src, shared_templates_dest, dirs_exist_ok=True)

            for src in skills:
                src = Path(src)
                templates_dest = self._work_dir / _SKILLS_SUBDIR / src.name / _SKILL_REFERENCES_TEMPLATE_SUBDIR
                templates_dest.mkdir(parents=True, exist_ok=True)
                shutil.copytree(templates_src, templates_dest, dirs_exist_ok=True)

        # ------------------------------------------------------------------
        # Build sandbox toolset
        # ------------------------------------------------------------------
        config = SandboxConfig(mounts=[
            Mount(host_path=self._work_dir, mount_point="/", mode="rw"),
        ])
        sandbox_toolset = FileSystemToolset(Sandbox(config))

        caller_toolsets = list(kwargs.pop("toolsets", None) or [])
        kwargs["toolsets"] = [sandbox_toolset] + caller_toolsets

        # ------------------------------------------------------------------
        # Build skills capability (always points at the fixed subdir)
        # ------------------------------------------------------------------
        caller_capabilities = list(kwargs.pop("capabilities", None) or [])
        has_skills = bool(skills)
        if has_skills:
            skills_dest.mkdir(parents=True, exist_ok=True)
            caller_capabilities = (
                [SkillsCapability(directories=[skills_dest])] + caller_capabilities
            )
        kwargs["capabilities"] = caller_capabilities

        # ------------------------------------------------------------------
        # Build instructions
        # ------------------------------------------------------------------
        caller_instructions: str | None = kwargs.pop("instructions", None)

        suffix = "\n\n" + _FILESYSTEM_INSTRUCTIONS

        if caller_instructions:
            combined_instructions = caller_instructions.rstrip() + suffix
        else:
            combined_instructions = _DEFAULT_PERSONALITY + suffix

        kwargs["instructions"] = combined_instructions

        super().__init__(model, **kwargs)

    @property
    def work_dir(self) -> Path:
        """The sandbox working directory (read-only).

        This is the host filesystem path mounted as virtual root '/' inside
        the sandboxed environment. If no work_dir was provided during
        initialization, this will be an auto-created temporary directory that
        is cleaned up when the agent is garbage collected or cleanup() is called.
        """
        return self._work_dir

    def cleanup(self) -> None:
        """Explicitly clean up the work directory if it was auto-created.

        If work_dir was provided by the caller, this method does nothing.
        Safe to call multiple times.

        The cleanup also happens automatically when the agent is garbage
        collected via __del__, but calling this method explicitly gives
        deterministic cleanup timing.
        """
        if self._owns_work_dir and self._work_dir.exists():
            shutil.rmtree(self._work_dir, ignore_errors=True)

    def __del__(self) -> None:
        """Clean up auto-created temp directory on garbage collection."""
        try:
            self.cleanup()
        except Exception:
            # Ignore all errors during interpreter shutdown when modules
            # may already be partially torn down.
            pass
