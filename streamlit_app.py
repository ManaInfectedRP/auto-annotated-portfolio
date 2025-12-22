from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import streamlit as st
import yaml


BASE_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = BASE_DIR / "content" / "pages" / "projects"


@dataclass
class Project:
    title: str
    description: str
    date: Optional[str]
    client: Optional[str]
    image_path: Optional[Path]
    slug: str
    body: str


def parse_frontmatter(path: Path) -> Tuple[dict, str]:
    """Parse YAML frontmatter from a Markdown file.

    Returns (metadata, body_markdown).
    """

    text = path.read_text(encoding="utf-8")

    # Expecting the file to start with --- for frontmatter
    stripped = text.lstrip()
    if not stripped.startswith("---"):
        return {}, text

    # Split on the first two occurrences of ---
    parts = stripped.split("---", 2)
    if len(parts) < 3:
        return {}, text

    _, fm_text, body = parts
    meta = yaml.safe_load(fm_text) or {}
    return meta, body.lstrip("\n")


def load_projects() -> List[Project]:
    """Load all project Markdown files from content/pages/projects.

    Any new .md file you add to that folder (except index.md) will
    automatically be picked up and shown in the carousel.
    """

    projects: List[Project] = []

    if not PROJECTS_DIR.exists():
        return projects

    for md_path in sorted(PROJECTS_DIR.glob("*.md")):
        # Skip the listing page itself
        if md_path.name.lower() == "index.md":
            continue

        meta, body = parse_frontmatter(md_path)

        title = meta.get("title", md_path.stem.replace("-", " ").title())
        description = (meta.get("description") or "").strip()
        date = meta.get("date")
        client = meta.get("client")

        # Try to resolve the featured image path from the Next.js public folder
        image_path: Optional[Path] = None
        featured = meta.get("featuredImage") or {}
        if isinstance(featured, dict):
            img_url = featured.get("url")
            if img_url:
                # Example: /images/featured-Image1.jpg → public/images/featured-Image1.jpg
                relative = img_url.lstrip("/")
                candidate = BASE_DIR / "public" / relative
                if candidate.exists():
                    image_path = candidate

        projects.append(
            Project(
                title=title,
                description=description,
                date=date,
                client=client,
                image_path=image_path,
                slug=md_path.stem,
                body=body,
            )
        )

    # Sort by date (newest first) if available
    def sort_key(p: Project):
        if p.date:
            try:
                return datetime.fromisoformat(p.date)
            except ValueError:
                return datetime.min
        return datetime.min

    projects.sort(key=sort_key, reverse=True)
    return projects


def render_project_card(project: Project) -> None:
    """Render a single project card inside a column."""

    if project.image_path and project.image_path.exists():
        st.image(str(project.image_path), use_column_width=True)

    st.subheader(project.title)

    meta_bits = []
    if project.client:
        meta_bits.append(project.client)
    if project.date:
        meta_bits.append(project.date)
    if meta_bits:
        # Use a simple ASCII separator between client and date
        st.caption(" | ".join(meta_bits))

    if project.description:
        st.write(project.description)

    with st.expander("Read more"):
        st.markdown(project.body)


def main() -> None:
    # Use a simple ASCII page icon to avoid encoding issues
    st.set_page_config(page_title="Sebastian Larsson - Projects", page_icon="SL", layout="wide")

    st.title("Projects Carousel")
    st.write(
        "Browse my projects three at a time. "
        "Whenever you add a new Markdown file to `content/pages/projects`, it will "
        "automatically appear in this carousel."
    )

    projects = load_projects()

    if not projects:
        st.info("No projects found in `content/pages/projects`. Add some .md files to get started.")
        return

    total = len(projects)
    visible_count = 3 if total >= 3 else total

    # Initialize the carousel index in session state
    if "carousel_index" not in st.session_state:
        st.session_state.carousel_index = 0

    # Navigation controls
    nav_prev, _, nav_next = st.columns([1, 6, 1])

    with nav_prev:
        if st.button("Previous", use_container_width=True):
            st.session_state.carousel_index = (st.session_state.carousel_index - visible_count) % total

    with nav_next:
        if st.button("Next", use_container_width=True):
            st.session_state.carousel_index = (st.session_state.carousel_index + visible_count) % total

    start = st.session_state.carousel_index
    indices = [(start + i) % total for i in range(visible_count)]

    cols = st.columns(visible_count)
    for col, idx in zip(cols, indices):
        with col:
            render_project_card(projects[idx])


if __name__ == "__main__":
    main()
