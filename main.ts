// The Monday Ledger — make.fun news-image-20261123 entrypoint.
//
// The poster is drawn offline by draw.py (Pillow, deterministic) and committed
// as entry.png. This program only copies it to the grader's output directory,
// because the grading run has no network and no third-party packages.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
console.log("entry.png copied to " + outDir);
