// The Friday Edition — V6 (Node 22, standard library only).
// The entry image lives beside this file; the program copies it to the
// grader's output directory. No network, no writes anywhere else.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
writeFileSync(
  join(outDir, "entry.png"),
  readFileSync(join(here, "entry.png")),
);
