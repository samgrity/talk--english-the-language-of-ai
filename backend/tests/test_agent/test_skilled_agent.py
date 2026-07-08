"""Tests for SkilledAgent and the underlying sandboxed filesystem.

Filesystem-level tests use the library's Sandbox/FileSystemToolset directly
(no LLM needed). Agent-level tests use Pydantic AI's TestModel to avoid
real API calls.
"""

import tempfile
from pathlib import Path

import pytest
from pydantic_ai.models.test import TestModel
from pydantic_ai_filesystem_sandbox import FileSystemToolset, Sandbox, SandboxConfig, Mount

import agent.skilled_agent as skilled_agent_module
from agent.skilled_agent import SkilledAgent, _DEFAULT_PERSONALITY, _FILESYSTEM_INSTRUCTIONS
from app.core.config import settings

MINIMAL_SKILL = """\
---
name: test-skill
description: A minimal skill used only in tests.
---

# Test Skill

## When to Use This Skill

Use this skill when testing skill loading behavior.

## Instructions

1. This is step one.
2. This is step two.
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_toolset(tmp: str | Path, mode: str = "rw") -> FileSystemToolset:
    config = SandboxConfig(mounts=[
        Mount(host_path=Path(tmp), mount_point="/", mode=mode),
    ])
    return FileSystemToolset(Sandbox(config))


def make_skill_dir(parent: Path, name: str = "test-skill") -> Path:
    """Write a minimal skill directory under parent and return its path."""
    skill_dir = parent / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(MINIMAL_SKILL)
    return skill_dir


def make_agent(tmp_path, skills=None, **kwargs) -> SkilledAgent:
    return SkilledAgent(
        model=settings.ai_model,
        work_dir=tmp_path,
        skills=skills,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# FileSystemToolset / Sandbox integration tests (no LLM)
# ---------------------------------------------------------------------------

class TestSandboxedFilesystem:

    def test_write_and_read_file(self, tmp_path):
        toolset = make_toolset(tmp_path)
        toolset.write("/hello.txt", "Hello, World!")
        result = toolset.read("/hello.txt")
        assert result.content == "Hello, World!"

    def test_read_truncates_at_max_chars(self, tmp_path):
        toolset = make_toolset(tmp_path)
        content = "x" * 100
        toolset.write("/big.txt", content)
        result = toolset.read("/big.txt", max_chars=10)
        assert len(result.content) == 10
        assert result.truncated is True
        assert result.total_chars == 100

    def test_write_creates_parent_directories(self, tmp_path):
        toolset = make_toolset(tmp_path)
        toolset.write("/a/b/c/file.txt", "deep")
        assert (tmp_path / "a" / "b" / "c" / "file.txt").read_text() == "deep"

    def test_list_files(self, tmp_path):
        toolset = make_toolset(tmp_path)
        toolset.write("/file1.txt", "c1")
        toolset.write("/sub/file2.txt", "c2")
        paths = toolset.list_files("/")
        assert "/file1.txt" in paths
        assert "/sub/file2.txt" in paths

    def test_delete_file(self, tmp_path):
        toolset = make_toolset(tmp_path)
        toolset.write("/del.txt", "bye")
        toolset.delete("/del.txt")
        assert not (tmp_path / "del.txt").exists()

    def test_edit_file(self, tmp_path):
        toolset = make_toolset(tmp_path)
        toolset.write("/edit.txt", "Hello World")
        toolset.edit("/edit.txt", old_text="World", new_text="Agent")
        result = toolset.read("/edit.txt")
        assert result.content == "Hello Agent"

    def test_copy_file(self, tmp_path):
        toolset = make_toolset(tmp_path)
        toolset.write("/src.txt", "original")
        toolset.copy("/src.txt", "/dst.txt")
        assert toolset.read("/dst.txt").content == "original"
        assert toolset.read("/src.txt").content == "original"

    def test_move_file(self, tmp_path):
        toolset = make_toolset(tmp_path)
        toolset.write("/before.txt", "data")
        toolset.move("/before.txt", "/after.txt")
        assert toolset.read("/after.txt").content == "data"
        assert not (tmp_path / "before.txt").exists()

    def test_read_only_mount_rejects_writes(self, tmp_path):
        toolset = make_toolset(tmp_path, mode="ro")
        with pytest.raises(Exception, match="read-only"):
            toolset.write("/blocked.txt", "oops")

    def test_path_traversal_rejected(self, tmp_path):
        toolset = make_toolset(tmp_path)
        with pytest.raises(Exception, match="outside sandbox"):
            toolset.read("/../../../etc/passwd")


# ---------------------------------------------------------------------------
# SkilledAgent tests using TestModel (no API calls)
# ---------------------------------------------------------------------------

class TestSkilledAgent:

    @pytest.mark.asyncio
    async def test_has_filesystem_and_skills_tools(self, tmp_path, tmp_path_factory):
        """All filesystem tools AND all skills tools should be registered."""
        skill_src = tmp_path_factory.mktemp("skill_src")
        skill_dir = make_skill_dir(skill_src)
        model = TestModel(call_tools=[])
        agent = make_agent(tmp_path, skills=[skill_dir])

        with agent.override(model=model):
            await agent.run("Do nothing")

        registered = {t.name for t in model.last_model_request_parameters.function_tools}
        expected_fs = {"read_file", "write_file", "edit_file", "delete_file",
                       "move_file", "copy_file", "list_files"}
        expected_skills = {"list_skills", "load_skill", "read_skill_resource", "run_skill_script"}
        assert expected_fs | expected_skills == registered

    @pytest.mark.asyncio
    async def test_without_skills(self, tmp_path):
        """skills=None should register only filesystem tools."""
        model = TestModel(call_tools=[])
        agent = make_agent(tmp_path, skills=None)

        with agent.override(model=model):
            await agent.run("Do nothing")

        registered = {t.name for t in model.last_model_request_parameters.function_tools}
        assert "load_skill" not in registered
        assert "read_file" in registered

    @pytest.mark.asyncio
    async def test_run_returns_output(self, tmp_path, tmp_path_factory):
        """TestModel returns a stub response without raising."""
        skill_src = tmp_path_factory.mktemp("skill_src")
        skill_dir = make_skill_dir(skill_src)
        agent = make_agent(tmp_path, skills=[skill_dir])
        with agent.override(model=TestModel(call_tools=[])):
            result = await agent.run("Say hello")
        assert result.output is not None

    def test_independent_workdirs(self, tmp_path):
        """Two agents with different work dirs must not share filesystem state."""
        with tempfile.TemporaryDirectory() as tmp2:
            make_agent(tmp_path)
            make_agent(tmp2)
            (tmp_path / "shared_name.txt").write_text("from agent1")
            assert not (Path(tmp2) / "shared_name.txt").exists()

    def test_skills_copied_into_work_dir(self, tmp_path, tmp_path_factory):
        """Skill directories are copied under <work_dir>/.agent/skills/<name>."""
        skill_src = tmp_path_factory.mktemp("skill_src")
        skill_dir = make_skill_dir(skill_src, name="my-skill")

        make_agent(tmp_path, skills=[skill_dir])

        dest = tmp_path / ".agent" / "skills" / "my-skill" / "SKILL.md"
        assert dest.exists()
        assert dest.read_text() == MINIMAL_SKILL

    def test_skill_name_preserved(self, tmp_path, tmp_path_factory):
        """The skill directory name is preserved when copied."""
        skill_src = tmp_path_factory.mktemp("skill_src")
        skill_dir = make_skill_dir(skill_src, name="custom-name")

        make_agent(tmp_path, skills=[skill_dir])

        assert (tmp_path / ".agent" / "skills" / "custom-name").is_dir()

    def test_multiple_skills_all_copied(self, tmp_path, tmp_path_factory):
        """All entries in the skills list are copied."""
        skill_src = tmp_path_factory.mktemp("skill_src")
        dirs = [make_skill_dir(skill_src, name=f"skill-{i}") for i in range(3)]

        make_agent(tmp_path, skills=dirs)

        skills_root = tmp_path / ".agent" / "skills"
        for i in range(3):
            assert (skills_root / f"skill-{i}").is_dir()

    def test_skill_subdirs_preserved(self, tmp_path, tmp_path_factory):
        """Nested files inside a skill (e.g. references/) are preserved."""
        skill_src = tmp_path_factory.mktemp("skill_src")
        skill_dir = make_skill_dir(skill_src, name="rich-skill")
        refs = skill_dir / "references"
        refs.mkdir()
        (refs / "spec.md").write_text("# Spec")

        make_agent(tmp_path, skills=[skill_dir])

        assert (tmp_path / ".agent" / "skills" / "rich-skill" / "references" / "spec.md").exists()

    def test_templates_copied_into_references_template_dir(self, tmp_path, tmp_path_factory):
        """Root templates should be copied to .agent/skills/references/template/."""
        skill_src = tmp_path_factory.mktemp("skill_src")
        skill_dir = make_skill_dir(skill_src, name="my-skill")

        make_agent(tmp_path, skills=[skill_dir])

        templates_dir = tmp_path / ".agent" / "skills" / "references" / "template"
        assert templates_dir.exists()
        assert (templates_dir / "registration_approval.txt").exists()

    def test_raises_if_templates_dir_missing(self, tmp_path, tmp_path_factory, monkeypatch):
        """Agent initialization should fail if root templates directory is missing."""
        skill_src = tmp_path_factory.mktemp("skill_src")
        skill_dir = make_skill_dir(skill_src, name="my-skill")

        missing_templates = tmp_path / "not-here"
        monkeypatch.setattr(skilled_agent_module, "_TEMPLATES_SOURCE_DIR", missing_templates)

        with pytest.raises(FileNotFoundError, match="Required templates directory not found"):
            make_agent(tmp_path, skills=[skill_dir])

    def test_default_instructions_when_none_provided(self, tmp_path):
        """Without caller instructions, default personality + fs suffix is used."""
        agent = make_agent(tmp_path)
        instructions = "\n".join(agent._instructions)
        assert _DEFAULT_PERSONALITY in instructions
        assert _FILESYSTEM_INSTRUCTIONS in instructions

    def test_caller_instructions_are_preserved(self, tmp_path):
        """Caller-provided instructions must appear in the final instructions."""
        custom = "You are a meticulous archivist."
        agent = make_agent(tmp_path, instructions=custom)
        instructions = "\n".join(agent._instructions)
        assert custom in instructions
        assert _FILESYSTEM_INSTRUCTIONS in instructions

    @pytest.mark.asyncio
    async def test_tool_decorator_works(self, tmp_path):
        """@agent.tool_plain decorator should register a custom tool."""
        agent = make_agent(tmp_path)

        @agent.tool_plain
        def my_custom_tool(x: int) -> int:
            """Double x."""
            return x * 2

        model = TestModel(call_tools=[])
        with agent.override(model=model):
            await agent.run("hi")

        registered = {t.name for t in model.last_model_request_parameters.function_tools}
        assert "my_custom_tool" in registered

    def test_skill_discovered_by_capability(self, tmp_path, tmp_path_factory):
        """SkillsCapability in the sandbox should discover the copied skill."""
        from pydantic_ai_skills import SkillsCapability

        skill_src = tmp_path_factory.mktemp("skill_src")
        skill_dir = make_skill_dir(skill_src, name="test-skill")

        make_agent(tmp_path, skills=[skill_dir])

        skills_dest = tmp_path / ".agent" / "skills"
        cap = SkillsCapability(directories=[skills_dest])
        assert "test-skill" in cap.toolset.skills


# ---------------------------------------------------------------------------
# Auto-created work_dir tests
# ---------------------------------------------------------------------------

class TestAutoWorkDir:

    def test_no_work_dir_creates_temp_directory(self):
        """SkilledAgent() with no work_dir creates a temp directory."""
        agent = SkilledAgent(model=settings.ai_model)
        try:
            assert agent.work_dir.exists()
            assert agent.work_dir.is_dir()
            assert "skilled-agent-" in agent.work_dir.name
        finally:
            agent.cleanup()

    def test_auto_work_dir_is_writable(self):
        """Auto-created work_dir should be writable."""
        agent = SkilledAgent(model=settings.ai_model)
        try:
            test_file = agent.work_dir / "test.txt"
            test_file.write_text("hello")
            assert test_file.read_text() == "hello"
        finally:
            agent.cleanup()

    def test_work_dir_property_returns_path(self):
        """work_dir property should return a Path instance."""
        agent = SkilledAgent(model=settings.ai_model)
        try:
            assert isinstance(agent.work_dir, Path)
        finally:
            agent.cleanup()

    def test_explicit_work_dir_accessible_via_property(self, tmp_path):
        """work_dir property should return the caller-provided path."""
        agent = make_agent(tmp_path)
        assert agent.work_dir == tmp_path

    def test_cleanup_removes_auto_created_dir(self):
        """cleanup() should remove auto-created temp directory."""
        agent = SkilledAgent(model=settings.ai_model)
        work_dir = agent.work_dir
        assert work_dir.exists()
        agent.cleanup()
        assert not work_dir.exists()

    def test_cleanup_does_not_remove_caller_provided_dir(self, tmp_path):
        """cleanup() should NOT remove a caller-provided work_dir."""
        agent = make_agent(tmp_path)
        (tmp_path / "keep.txt").write_text("keep me")
        agent.cleanup()
        assert tmp_path.exists()
        assert (tmp_path / "keep.txt").exists()

    def test_cleanup_is_idempotent(self):
        """Calling cleanup() multiple times should not raise."""
        agent = SkilledAgent(model=settings.ai_model)
        agent.cleanup()
        agent.cleanup()  # Should not raise

    def test_del_triggers_cleanup(self):
        """Deleting the agent should clean up auto-created work_dir."""
        import gc
        agent = SkilledAgent(model=settings.ai_model)
        work_dir = agent.work_dir
        assert work_dir.exists()
        del agent
        gc.collect()
        assert not work_dir.exists()

    def test_skills_copied_into_auto_work_dir(self, tmp_path_factory):
        """Skills should be copied into auto-created work_dir."""
        skill_src = tmp_path_factory.mktemp("skill_src")
        skill_dir = make_skill_dir(skill_src, name="auto-skill")

        agent = SkilledAgent(
            model=settings.ai_model,
            skills=[skill_dir],
        )
        try:
            skills_dest = agent.work_dir / ".agent" / "skills" / "auto-skill"
            assert skills_dest.exists()
            assert (skills_dest / "SKILL.md").exists()
        finally:
            agent.cleanup()

    @pytest.mark.asyncio
    async def test_auto_work_dir_with_testmodel(self, tmp_path_factory):
        """Auto work_dir should work end-to-end with TestModel."""
        skill_src = tmp_path_factory.mktemp("skill_src")
        skill_dir = make_skill_dir(skill_src)

        agent = SkilledAgent(
            model=settings.ai_model,
            skills=[skill_dir],
        )
        try:
            model = TestModel(call_tools=[])
            with agent.override(model=model):
                result = await agent.run("Test")
            assert result.output is not None
        finally:
            agent.cleanup()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
