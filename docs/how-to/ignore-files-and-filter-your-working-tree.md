# Ignore files and filter your working tree

Use `.loreignore` to keep new build artifacts and temporary files out of status, staging, and commits. Use a view filter to keep selected committed paths out of your local working tree. This guide assumes you already have a Lore repository.

## Prerequisites

- The `lore` CLI on your PATH. See [Install the Lore CLI](install-lore-cli.md).
- A terminal in your repository's root directory.

## Ignore build artifacts

1. **Add rules to `.loreignore`.**

   Create `.loreignore` in the repository root, or append to the existing file. For an Unreal Engine project, start with:

   ```text
   Binaries/
   Intermediate/
   Saved/
   DerivedDataCache/
   *.tmp
   ```

   These rules exclude generated directories and temporary files from local scans. Keep source files and project configuration outside these patterns.

2. **Check the filtered status.**

   ```bash
   lore status --scan
   ```

   New files under `Source/` and `Config/` still appear, along with `.loreignore`. Files matching the ignore rules don't appear.

3. **Stage and review the files you want to commit.**

   ```bash
   lore stage --scan .
   lore status
   ```

   The `.` selects the repository root. Check the staged paths before committing.

4. **Commit the files and ignore rules.**

   ```bash
   lore commit "Track source files and ignore build artifacts"
   ```

   Committing `.loreignore` shares the rules with other users of the repository.

Ignore rules filter outbound content. They don't remove files from existing revisions or stop sync from bringing committed files into your working tree. To leave committed paths out of a local working tree, use a view.

## Narrow your local view

A view filter controls which committed paths Lore writes to disk. It also limits the paths that status and staging consider. Each repository instance has its own view; the view isn't part of a commit.

Commit your working changes before narrowing the view. Lore removes committed files that leave the view from the working tree. Those files remain in the repository's revisions.

1. **Create a view file outside the repository.**

   Save a file named `narrow.view` with this content to exclude a large asset directory:

   ```text
   /Content/Bulk/
   ```

   Replace `Content/Bulk` with the repository path you want to exclude. This file defines the new view; it doesn't add to an existing view's rules.

2. **Apply the view to the existing instance.**

   Replace `/absolute/path/narrow.view` with your view file's absolute path:

   ```bash
   lore sync --view "/absolute/path/narrow.view"
   ```

   Lore removes committed files under `Content/Bulk/` from disk and keeps the other committed paths in the working tree. Ignored local build artifacts remain on disk.

3. **Restore the full view when needed.**

   Create an empty file named `full.view` outside the repository, then replace the path in this command with its absolute path:

   ```bash
   lore sync --view "/absolute/path/full.view"
   ```

   Lore restores the committed files that the narrower view excluded.

## Result

Your ignore rules keep generated files out of commits, and your local view controls which committed files occupy the working tree.

## See also

- [Lore CLI commands](../reference/lore-cli-commands.md) — command syntax and options.
- [Views and ignore rules](../explanation/system-design.md#12-sparseness-and-partial-working-copies) — how filters apply to local and committed state.
