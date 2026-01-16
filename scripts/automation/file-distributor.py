#!/usr/bin/env python3
"""
Enterprise File Distributor (Python)

Purpose
- Select a source file and a root folder via GUI.
- Configure options via GUI:
  - Dry run
  - Overwrite
  - Depth (0..N, or -1 for full recursive)
  - Confirm each folder
  - Include hidden folders
  - Audit log folder
- Copy the source file into each eligible folder.
- Emit audit logs to CSV and JSON.

Notes
- Uses Tkinter (standard library) for GUI.
- Designed for controlled execution and auditability.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import shutil
import sys
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
except Exception as e:
    raise SystemExit(f"Tkinter is required but not available: {e}")


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def default_log_dir() -> Path:
    home = Path.home()
    base = home / "Documents" / "FileDistributorLogs"
    ensure_dir(base)
    return base


def enumerate_folders_by_depth(root: Path, depth: int, include_hidden: bool = True) -> List[Path]:
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Root directory not found: {root}")

    folders: List[Path] = [root]

    if depth == 0:
        return folders

    def is_hidden(p: Path) -> bool:
        """Check if a path is hidden (cross-platform)"""
        if not include_hidden:
            # Unix-like systems: starts with dot
            if p.name.startswith('.'):
                return True
            # Windows: check hidden attribute
            if os.name == 'nt':
                try:
                    import stat
                    return bool(p.stat().st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
                except (AttributeError, OSError):
                    pass
        return False

    if depth == -1:
        for d, subdirs, _files in os.walk(root):
            current_dir = Path(d)
            # Add the current directory if it's not the root (root is already added)
            if current_dir != root:
                folders.append(current_dir)
            # Filter hidden subdirectories in-place if needed
            if not include_hidden:
                subdirs[:] = [sd for sd in subdirs if not is_hidden(current_dir / sd)]
        return folders

    if depth < -1:
        raise ValueError("Depth must be -1 (full recursive) or 0..N")

    # BFS by depth
    current_level: List[Path] = [root]
    for _level in range(1, depth + 1):
        next_level: List[Path] = []
        for parent in current_level:
            try:
                for child in parent.iterdir():
                    if child.is_dir() and not is_hidden(child):
                        folders.append(child)
                        next_level.append(child)
            except PermissionError:
                # Skip restricted folders, still auditable in error records later if desired
                continue
        if not next_level:
            break
        current_level = next_level

    return folders


@dataclass
class Options:
    dry_run: bool
    overwrite: bool
    depth: int
    confirm_each: bool
    include_hidden: bool
    log_folder: Path


@dataclass
class AuditRecord:
    run_id: str
    timestamp: str
    folder: str
    target_path: str
    action_planned: str
    action_taken: str
    decision: str
    dry_run: bool
    overwrite: bool
    depth: int
    source_file: str
    source_size: int
    source_sha256: str
    result: str
    error: str


class OptionsDialog(tk.Toplevel):
    def __init__(self, master: tk.Tk, source_file: Path, root_dir: Path):
        super().__init__(master)
        self.title("Distribution Options")
        self.resizable(False, False)
        self.source_file = source_file
        self.root_dir = root_dir

        self.result: Optional[Options] = None

        self.var_dry_run = tk.BooleanVar(value=True)
        self.var_overwrite = tk.BooleanVar(value=False)
        self.var_confirm_each = tk.BooleanVar(value=False)
        self.var_include_hidden = tk.BooleanVar(value=True)
        self.var_depth = tk.IntVar(value=1)

        self.var_log_folder = tk.StringVar(value=str(default_log_dir()))

        self._build_ui()

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _build_ui(self) -> None:
        padx = 10
        pady = 6

        frm = tk.Frame(self)
        frm.pack(fill="both", expand=True, padx=padx, pady=padx)

        lbl_src = tk.Label(frm, text=f"Source file:\n{self.source_file}", justify="left", anchor="w")
        lbl_src.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, pady))

        lbl_root = tk.Label(frm, text=f"Root folder:\n{self.root_dir}", justify="left", anchor="w")
        lbl_root.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, pady))

        chk_dry = tk.Checkbutton(frm, text="Dry run (no files written)", variable=self.var_dry_run)
        chk_dry.grid(row=2, column=0, columnspan=3, sticky="w", pady=(0, pady))

        chk_over = tk.Checkbutton(frm, text="Overwrite if file exists", variable=self.var_overwrite)
        chk_over.grid(row=3, column=0, columnspan=3, sticky="w", pady=(0, pady))

        chk_confirm = tk.Checkbutton(
            frm,
            text="Confirm each folder (Yes, No, Yes to All, Cancel)",
            variable=self.var_confirm_each,
        )
        chk_confirm.grid(row=4, column=0, columnspan=3, sticky="w", pady=(0, pady))

        chk_hidden = tk.Checkbutton(frm, text="Include hidden folders", variable=self.var_include_hidden)
        chk_hidden.grid(row=5, column=0, columnspan=3, sticky="w", pady=(0, pady))

        grp_depth = tk.LabelFrame(frm, text="Child Folder Depth")
        grp_depth.grid(row=6, column=0, columnspan=3, sticky="we", pady=(pady, pady))
        tk.Label(grp_depth, text="Depth (0 = root only, -1 = full recursive):").grid(row=0, column=0, sticky="w", padx=8, pady=6)

        spn = tk.Spinbox(grp_depth, from_=-1, to=50, textvariable=self.var_depth, width=6)
        spn.grid(row=0, column=1, sticky="w", padx=8, pady=6)

        tk.Label(grp_depth, text="0=root only, 1=root + 1 level, -1=full recursive").grid(
            row=0, column=2, sticky="w", padx=8, pady=6
        )

        grp_log = tk.LabelFrame(frm, text="Audit Logging")
        grp_log.grid(row=7, column=0, columnspan=3, sticky="we", pady=(pady, pady))

        tk.Label(grp_log, text="Log folder:").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        ent_log = tk.Entry(grp_log, textvariable=self.var_log_folder, width=70)
        ent_log.grid(row=0, column=1, sticky="we", padx=8, pady=6)

        btn_browse = tk.Button(grp_log, text="Browse", command=self._browse_log_folder)
        btn_browse.grid(row=0, column=2, sticky="e", padx=8, pady=6)

        grp_log.columnconfigure(1, weight=1)

        btn_run = tk.Button(frm, text="Run", width=10, command=self._on_ok)
        btn_run.grid(row=8, column=1, sticky="e", padx=8, pady=(10, 0))

        btn_cancel = tk.Button(frm, text="Cancel", width=10, command=self._on_cancel)
        btn_cancel.grid(row=8, column=2, sticky="e", padx=8, pady=(10, 0))

    def _browse_log_folder(self) -> None:
        chosen = filedialog.askdirectory(title="Select a folder for audit logs")
        if chosen:
            self.var_log_folder.set(chosen)

    def _on_ok(self) -> None:
        log_folder = Path(self.var_log_folder.get().strip())
        if not str(log_folder):
            messagebox.showerror("Validation", "Log folder is required for audit readiness.")
            return
        try:
            ensure_dir(log_folder)
        except Exception as e:
            messagebox.showerror("Validation", f"Unable to create or access log folder: {e}")
            return

        self.result = Options(
            dry_run=bool(self.var_dry_run.get()),
            overwrite=bool(self.var_overwrite.get()),
            depth=int(self.var_depth.get()),
            confirm_each=bool(self.var_confirm_each.get()),
            include_hidden=bool(self.var_include_hidden.get()),
            log_folder=log_folder,
        )
        self.destroy()

    def _on_cancel(self) -> None:
        self.result = None
        self.destroy()


def select_source_file(root: tk.Tk) -> Path:
    path = filedialog.askopenfilename(title="Select the source file to distribute")
    if not path:
        raise RuntimeError("No source file selected.")
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise RuntimeError(f"Source file not found: {p}")
    return p


def select_root_folder(root: tk.Tk) -> Path:
    path = filedialog.askdirectory(title="Select the root directory")
    if not path:
        raise RuntimeError("No root directory selected.")
    p = Path(path)
    if not p.exists() or not p.is_dir():
        raise RuntimeError(f"Root directory not found: {p}")
    return p


def confirm_folder(
    folder: Path,
    target_path: Path,
    source_name: str,
    overwrite: bool,
    exists: bool,
) -> str:
    """
    Returns decision:
      - "yes"
      - "no"
      - "yes_all"
      - "cancel"
    """
    action = "OVERWRITE" if exists and overwrite else ("SKIP" if exists else "COPY")

    msg = "\n".join(
        [
            "Target folder:",
            str(folder),
            "",
            "File:",
            source_name,
            "",
            "Target path:",
            str(target_path),
            "",
            f"Planned action: {action}",
            "",
            "Select Yes to proceed, No to skip, Yes to All to proceed without further prompts, Cancel to abort.",
        ]
    )

    # Tkinter has no native Yes to All. Implement via custom dialog.
    dlg = tk.Toplevel()
    dlg.title("Confirm Folder")
    dlg.resizable(False, False)
    dlg.grab_set()

    decision_var = tk.StringVar(value="cancel")

    txt = tk.Label(dlg, text=msg, justify="left", anchor="w")
    txt.pack(padx=12, pady=10)

    btn_frame = tk.Frame(dlg)
    btn_frame.pack(padx=12, pady=(0, 12), fill="x")

    def set_decision(val: str) -> None:
        decision_var.set(val)
        dlg.destroy()

    tk.Button(btn_frame, text="Yes", width=10, command=lambda: set_decision("yes")).pack(side="left", padx=6)
    tk.Button(btn_frame, text="No", width=10, command=lambda: set_decision("no")).pack(side="left", padx=6)
    tk.Button(btn_frame, text="Yes to All", width=12, command=lambda: set_decision("yes_all")).pack(side="left", padx=6)
    tk.Button(btn_frame, text="Cancel", width=10, command=lambda: set_decision("cancel")).pack(side="right", padx=6)

    dlg.wait_window()
    return decision_var.get()


def write_audit_logs(records: List[AuditRecord], csv_path: Path, json_path: Path) -> None:
    ensure_dir(csv_path.parent)
    ensure_dir(json_path.parent)

    # CSV
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(records[0]).keys()) if records else list(asdict(AuditRecord(
            run_id="",
            timestamp="",
            folder="",
            target_path="",
            action_planned="",
            action_taken="",
            decision="",
            dry_run=False,
            overwrite=False,
            depth=0,
            source_file="",
            source_size=0,
            source_sha256="",
            result="",
            error="",
        )).keys()))
        writer.writeheader()
        for r in records:
            writer.writerow(asdict(r))

    # JSON
    with json_path.open("w", encoding="utf-8") as f:
        json.dump([asdict(r) for r in records], f, indent=2)


def distribute_file(source_file: Path, root_dir: Path, opts: Options) -> Tuple[Dict[str, object], Path, Path]:
    run_id = str(uuid.uuid4())
    started_at = iso_now()

    source_size = source_file.stat().st_size
    source_hash = sha256_file(source_file)
    source_name = source_file.name

    folders = enumerate_folders_by_depth(root_dir, opts.depth, opts.include_hidden)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = opts.log_folder / f"file-distributor_{stamp}.csv"
    json_path = opts.log_folder / f"file-distributor_{stamp}.json"

    records: List[AuditRecord] = []

    stats: Dict[str, object] = {
        "run_id": run_id,
        "started_at": started_at,
        "ended_at": "",
        "total_folders": len(folders),
        "copied": 0,
        "overwritten": 0,
        "skipped_exists": 0,
        "skipped_user": 0,
        "errors": 0,
        "cancelled": False,
        "dry_run": opts.dry_run,
        "overwrite": opts.overwrite,
        "depth": opts.depth,
        "confirm_each": opts.confirm_each,
        "include_hidden": opts.include_hidden,
        "source_file": str(source_file),
        "root_dir": str(root_dir),
        "platform": platform.platform(),
        "python": sys.version.split()[0],
    }

    yes_to_all = False

    for folder in folders:
        target_path = folder / source_name
        exists = target_path.exists() and target_path.is_file()

        if exists and not opts.overwrite:
            planned = "SkipExists"
        elif exists and opts.overwrite:
            planned = "Overwrite"
        else:
            planned = "Copy"

        decision = "auto"
        taken = "planned"

        try:
            if opts.confirm_each and not yes_to_all:
                d = confirm_folder(folder, target_path, source_name, opts.overwrite, exists)
                if d == "no":
                    stats["skipped_user"] = int(stats["skipped_user"]) + 1
                    decision = "user_no"
                    records.append(AuditRecord(
                        run_id=run_id,
                        timestamp=iso_now(),
                        folder=str(folder),
                        target_path=str(target_path),
                        action_planned=planned,
                        action_taken="Skip",
                        decision=decision,
                        dry_run=opts.dry_run,
                        overwrite=opts.overwrite,
                        depth=opts.depth,
                        source_file=str(source_file),
                        source_size=source_size,
                        source_sha256=source_hash,
                        result="SkippedByUser",
                        error="",
                    ))
                    continue
                if d == "cancel":
                    stats["cancelled"] = True
                    decision = "user_cancel"
                    records.append(AuditRecord(
                        run_id=run_id,
                        timestamp=iso_now(),
                        folder=str(folder),
                        target_path=str(target_path),
                        action_planned=planned,
                        action_taken="Abort",
                        decision=decision,
                        dry_run=opts.dry_run,
                        overwrite=opts.overwrite,
                        depth=opts.depth,
                        source_file=str(source_file),
                        source_size=source_size,
                        source_sha256=source_hash,
                        result="Cancelled",
                        error="",
                    ))
                    break
                if d == "yes_all":
                    yes_to_all = True
                    decision = "user_yes_all"
                else:
                    decision = "user_yes"

            if exists and not opts.overwrite:
                stats["skipped_exists"] = int(stats["skipped_exists"]) + 1
                records.append(AuditRecord(
                    run_id=run_id,
                    timestamp=iso_now(),
                    folder=str(folder),
                    target_path=str(target_path),
                    action_planned="SkipExists",
                    action_taken="Skip",
                    decision=decision,
                    dry_run=opts.dry_run,
                    overwrite=opts.overwrite,
                    depth=opts.depth,
                    source_file=str(source_file),
                    source_size=source_size,
                    source_sha256=source_hash,
                    result="SkippedExists",
                    error="",
                ))
                continue

            if opts.dry_run:
                if exists and opts.overwrite:
                    stats["overwritten"] = int(stats["overwritten"]) + 1
                    taken = "WouldOverwrite"
                else:
                    stats["copied"] = int(stats["copied"]) + 1
                    taken = "WouldCopy"

                records.append(AuditRecord(
                    run_id=run_id,
                    timestamp=iso_now(),
                    folder=str(folder),
                    target_path=str(target_path),
                    action_planned=planned,
                    action_taken=taken,
                    decision=decision,
                    dry_run=opts.dry_run,
                    overwrite=opts.overwrite,
                    depth=opts.depth,
                    source_file=str(source_file),
                    source_size=source_size,
                    source_sha256=source_hash,
                    result="DryRun",
                    error="",
                ))
                continue

            # Real write
            ensure_dir(folder)
            if exists and opts.overwrite:
                shutil.copy2(source_file, target_path)
                stats["overwritten"] = int(stats["overwritten"]) + 1
                taken = "Overwrite"
            else:
                shutil.copy2(source_file, target_path)
                stats["copied"] = int(stats["copied"]) + 1
                taken = "Copy"

            records.append(AuditRecord(
                run_id=run_id,
                timestamp=iso_now(),
                folder=str(folder),
                target_path=str(target_path),
                action_planned=planned,
                action_taken=taken,
                decision=decision,
                dry_run=opts.dry_run,
                overwrite=opts.overwrite,
                depth=opts.depth,
                source_file=str(source_file),
                source_size=source_size,
                source_sha256=source_hash,
                result="Success",
                error="",
            ))

        except Exception as e:
            stats["errors"] = int(stats["errors"]) + 1
            records.append(AuditRecord(
                run_id=run_id,
                timestamp=iso_now(),
                folder=str(folder),
                target_path=str(target_path),
                action_planned=planned,
                action_taken="Error",
                decision=decision,
                dry_run=opts.dry_run,
                overwrite=opts.overwrite,
                depth=opts.depth,
                source_file=str(source_file),
                source_size=source_size,
                source_sha256=source_hash,
                result="Error",
                error=str(e),
            ))

    stats["ended_at"] = iso_now()

    # Ensure logs exist even if no records, for audit readiness
    if not records:
        records.append(AuditRecord(
            run_id=run_id,
            timestamp=iso_now(),
            folder="",
            target_path="",
            action_planned="",
            action_taken="",
            decision="",
            dry_run=opts.dry_run,
            overwrite=opts.overwrite,
            depth=opts.depth,
            source_file=str(source_file),
            source_size=source_size,
            source_sha256=source_hash,
            result="NoOp",
            error="",
        ))

    write_audit_logs(records, csv_path, json_path)

    return stats, csv_path, json_path


def main() -> int:
    app = tk.Tk()
    app.withdraw()

    try:
        source_file = select_source_file(app)
        root_dir = select_root_folder(app)

        dlg = OptionsDialog(app, source_file, root_dir)
        app.wait_window(dlg)

        if dlg.result is None:
            raise RuntimeError("Operation cancelled.")

        opts = dlg.result

        stats, csv_path, json_path = distribute_file(source_file, root_dir, opts)

        summary = "\n".join(
            [
                f"RunId:        {stats['run_id']}",
                f"StartedAt:    {stats['started_at']}",
                f"EndedAt:      {stats['ended_at']}",
                f"TotalFolders: {stats['total_folders']}",
                f"Copied:       {stats['copied']}",
                f"Overwritten:  {stats['overwritten']}",
                f"SkippedExists:{stats['skipped_exists']}",
                f"SkippedUser:  {stats['skipped_user']}",
                f"Errors:       {stats['errors']}",
                f"Cancelled:    {stats['cancelled']}",
                "",
                f"Audit CSV:    {csv_path}",
                f"Audit JSON:   {json_path}",
            ]
        )

        messagebox.showinfo("Distribution Complete", summary)
        return 0

    except Exception as e:
        messagebox.showerror("Operation Result", str(e))
        return 1
    finally:
        try:
            app.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
