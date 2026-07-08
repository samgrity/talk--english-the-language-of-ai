import fs from "node:fs";
import path from "node:path";

const cssRoot = path.join(process.cwd(), ".next", "static", "css");

if (!fs.existsSync(cssRoot)) {
  console.error("Tailwind check failed: .next/static/css not found. Run `npm run build` first.");
  process.exit(1);
}

const cssFiles = fs.readdirSync(cssRoot).filter((name) => name.endsWith(".css"));

if (cssFiles.length === 0) {
  console.error("Tailwind check failed: no CSS files were generated.");
  process.exit(1);
}

const cssBundle = cssFiles
  .map((file) => fs.readFileSync(path.join(cssRoot, file), "utf8"))
  .join("\n");

const requiredSelectors = [
  ".bg-gray-50",
  ".rounded-lg",
  ".text-gray-900",
  ".flex",
];

const missing = requiredSelectors.filter((selector) => !cssBundle.includes(selector));

if (missing.length > 0) {
  console.error(`Tailwind check failed: missing selectors ${missing.join(", ")}`);
  process.exit(1);
}

console.log("Tailwind check passed: utility selectors are present in built CSS.");
