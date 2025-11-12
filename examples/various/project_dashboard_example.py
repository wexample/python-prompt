"""Project Dashboard Example - Display comprehensive project health and status."""

from __future__ import annotations

import os
import random
import subprocess
from pathlib import Path
from typing import Any

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.example.interactive_example import InteractiveExample


class ProjectDashboardExample(InteractiveExample):
    """Display comprehensive project information in a beautiful dashboard."""

    def __init__(self, project_path: str | None = None, **kwargs):
        """Initialize the dashboard.
        
        Args:
            project_path: Path to the project. Defaults to current directory.
            **kwargs: Additional arguments from the example system.
        """
        super().__init__(**kwargs)
        self.ensure_io_manager()
        self.project_path = Path(project_path or os.getcwd())
        self.project_name = self.project_path.name
        
    def _get_git_info(self) -> dict[str, str]:
        """Get git repository information."""
        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.project_path,
                stderr=subprocess.DEVNULL
            ).decode().strip()
            
            remote = subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"],
                cwd=self.project_path,
                stderr=subprocess.DEVNULL
            ).decode().strip()
            
            status = subprocess.check_output(
                ["git", "status", "--porcelain"],
                cwd=self.project_path,
                stderr=subprocess.DEVNULL
            ).decode().strip()
            
            return {
                "branch": branch,
                "remote": remote,
                "clean": len(status) == 0,
                "changes": len(status.split("\n")) if status else 0
            }
        except (subprocess.CalledProcessError, FileNotFoundError):
            return {
                "branch": "no-git",
                "remote": "none",
                "clean": True,
                "changes": 0
            }
    
    def _count_files(self, pattern: str) -> int:
        """Count files matching a pattern."""
        return len(list(self.project_path.rglob(pattern)))
    
    def _get_coverage(self) -> int:
        """Get test coverage percentage (simulated for demo)."""
        # In real implementation, parse coverage report
        return random.randint(70, 95)
    
    def _find_linked_libraries(self) -> list[str]:
        """Find linked local libraries."""
        libraries = []
        parent = self.project_path.parent
        
        if parent.exists():
            for item in parent.iterdir():
                if item.is_dir() and (item / "pyproject.toml").exists():
                    if item.name != self.project_name:
                        libraries.append(item.name)
        
        return sorted(libraries)
    
    def execute(self) -> None:
        """Display the complete project dashboard."""
        # Header
        self.io.title(text=f"@color:cyan+bold{{📊 Project Dashboard: {self.project_name}}}")
        self.io.log("")
        
        # === SECTION 1: Basic Information ===
        self.io.separator(label="@color:yellow+bold{📋 Basic Information}")
        
        version = "0.0.56"  # Could be read from pyproject.toml
        environment = os.getenv("ENVIRONMENT", "local")
        
        self.io.properties(
            properties={
                "Name": f"@color:cyan+bold{{{self.project_name}}}",
                "Version": f"@color:green{{{version}}}",
                "Path": f"@path:short{{{str(self.project_path)}}}",
                "Environment": f"@color:yellow{{{environment}}}",
            }
        )
        
        self.io.log("")
        
        # === SECTION 2: Code Quality Metrics ===
        self.io.separator(label="@color:blue+bold{🔬 Code Quality}")
        
        # Count various file types
        test_count = self._count_files("test_*.py")
        example_count = len(list((self.project_path / "examples").rglob("*.py"))) if (self.project_path / "examples").exists() else 0
        src_count = self._count_files("*.py")
        coverage = self._get_coverage()
        
        # Display metrics as properties
        self.io.properties(
            properties={
                "Python Files": f"@color:cyan{{{src_count}}} files",
                "Test Files": f"@color:green{{{test_count}}} tests" if test_count > 0 else "@color:red{0} tests",
                "Examples": f"@color:green{{{example_count}}} examples" if example_count > 0 else "@color:red{0} examples",
            }
        )
        
        # Coverage with progress bar
        self.io.log("")
        self.io.log("  @color:cyan+bold{Test Coverage:}")
        self.io.progress(
            label=f"  Coverage",
            total=100,
            current=coverage,
            color=TerminalColor.GREEN if coverage >= 80 else TerminalColor.YELLOW,
            show_percentage=True
        ).get_handle().finish()
        
        self.io.log("")
        
        # === SECTION 3: Git Status ===
        self.io.separator(label="@color:magenta+bold{🌿 Git Repository}")
        
        git_info = self._get_git_info()
        
        self.io.properties(
            properties={
                "Branch": f"@color:cyan{{{git_info['branch']}}}",
                "Remote": f"@path:short{{{git_info['remote']}}}",
                "Status": "@color:green{✓ Clean}" if git_info['clean'] else f"@color:yellow{{⚠ {git_info['changes']} changes pending}}",
            }
        )
        
        self.io.log("")
        
        # === SECTION 4: Health Overview ===
        self.io.separator(label="@color:green+bold{💚 Health Overview}")
        
        # Health indicators
        health_data = [
            ["Metric", "Status", "Score"],
            [
                "Tests",
                "@color:green{✓ Present}" if test_count > 0 else "@color:red{✗ Missing}",
                "@color:green{■■■■■}" if test_count > 0 else "@color:red{■}@color:gray{■■■■}"
            ],
            [
                "Coverage",
                f"@color:green{{{coverage}%}}" if coverage >= 80 else f"@color:yellow{{{coverage}%}}",
                "@color:green{■■■■■}" if coverage >= 80 else "@color:yellow{■■■■}@color:gray{■}"
            ],
            [
                "Examples",
                "@color:green{✓ Present}" if example_count > 0 else "@color:red{✗ Missing}",
                "@color:green{■■■■■}" if example_count > 0 else "@color:red{■}@color:gray{■■■■}"
            ],
            [
                "Git Clean",
                "@color:green{✓ Clean}" if git_info['clean'] else "@color:yellow{⚠ Dirty}",
                "@color:green{■■■■■}" if git_info['clean'] else "@color:yellow{■■■■}@color:gray{■}"
            ],
        ]
        
        self.io.table(
            data=health_data,
            title="Project Health Indicators"
        )
        
        self.io.log("")
        
        # === SECTION 5: Linked Libraries ===
        libraries = self._find_linked_libraries()
        
        if libraries:
            self.io.separator(label="@color:cyan+bold{📦 Linked Local Libraries}")
            
            self.io.log(f"  @color:gray{{Found {len(libraries)} linked libraries:}}")
            self.io.list(
                items=[f"@color:green{{✓}} @color:cyan{{{lib}}}" for lib in libraries]
            )
            
            self.io.log("")
        
        # === SECTION 6: Quick Actions ===
        self.io.separator(label="@color:yellow+bold{💡 Quick Actions}")
        
        self.io.suggestions(
            message="Suggested commands:",
            suggestions=[
                "@color:cyan{pytest -q} @color:gray{→ Run tests}",
                "@color:cyan{coverage run -m pytest && coverage report} @color:gray{→ Check coverage}",
                "@color:cyan{python -m examples} @color:gray{→ List examples}",
                "@color:cyan{git status} @color:gray{→ Check git status}",
            ]
        )
        
        self.io.log("")
        
        # === SECTION 7: Project Files ===
        self.io.separator(label="@color:blue+bold{📁 Important Files}")
        
        important_files = [
            ("README.md", "Documentation"),
            ("pyproject.toml", "Project config"),
            ("requirements.txt", "Dependencies"),
            (".gitignore", "Git config"),
            ("LICENSE", "License"),
        ]
        
        file_status = []
        for filename, description in important_files:
            file_path = self.project_path / filename
            if file_path.exists():
                file_status.append([
                    f"@color:green{{✓}}",
                    f"@path:short{{{filename}}}",
                    f"@color:gray{{{description}}}"
                ])
            else:
                file_status.append([
                    f"@color:red{{✗}}",
                    f"@color:gray{{{filename}}}",
                    f"@color:gray{{{description}}}"
                ])
        
        self.io.table(
            data=[["", "File", "Description"]] + file_status,
            title="File Checklist"
        )
        
        self.io.log("")
        
        # === Footer ===
        overall_health = (
            (100 if test_count > 0 else 0) +
            coverage +
            (100 if example_count > 0 else 0) +
            (100 if git_info['clean'] else 50)
        ) / 4
        
        if overall_health >= 80:
            self.io.success(message=f"@color:green+bold{{✓ Project health: {overall_health:.0f}%}} - Looking good! 🎉")
        elif overall_health >= 60:
            self.io.warning(message=f"@color:yellow+bold{{⚠ Project health: {overall_health:.0f}%}} - Some improvements needed")
        else:
            self.io.failure(message=f"@color:red+bold{{✗ Project health: {overall_health:.0f}%}} - Needs attention")
        
        self.io.log("")
        self.io.separator()

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Project Dashboard",
                "description": "Display comprehensive project health and status",
                "callback": self.execute,
            },
        ]
