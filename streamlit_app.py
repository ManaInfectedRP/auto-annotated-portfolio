from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import streamlit as st
import yaml


BASE_DIR = Path(__file__).resolve().parent
CONTENT_PAGES_DIR = BASE_DIR / "content" / "pages"
HOME_INDEX_PATH = CONTENT_PAGES_DIR / "index.md"
INFO_PAGE_PATH = CONTENT_PAGES_DIR / "info.md"
PROJECTS_DIR = CONTENT_PAGES_DIR / "projects"
PROJECTS_INDEX_PATH = PROJECTS_DIR / "index.md"


@dataclass
class Project:
    title: str
    description: str
    date: Optional[str]
    client: Optional[str]
    image_path: Optional[Path]
    slug: str
    body: str


@dataclass
class ProjectsPageConfig:
    title: str
    hero_title: Optional[str] = None
    hero_subtitle: Optional[str] = None


@dataclass
class HomeHero:
    title: str
    subtitle: Optional[str] = None


@dataclass
class InfoPageContent:
    title: str
    hero_text: Optional[str]
    skills: List[str]
    contact_markdown: Optional[str]
    experience_markdown: Optional[str]
    education_markdown: Optional[str]


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


def load_home_hero() -> HomeHero:
    """Load the main hero title/subtitle from content/pages/index.md."""

    if not HOME_INDEX_PATH.exists():
        return HomeHero(title="Hi, I'm Sebastian Larsson")

    meta, _ = parse_frontmatter(HOME_INDEX_PATH)

    hero_title: Optional[str] = None
    hero_subtitle: Optional[str] = None
    for section in meta.get("sections", []):
        if isinstance(section, dict) and section.get("type") == "HeroSection":
            hero_title = section.get("title") or hero_title
            hero_subtitle = section.get("subtitle") or hero_subtitle
            break

    if not hero_title:
        hero_title = meta.get("title", "Home")

    return HomeHero(title=hero_title, subtitle=hero_subtitle)


def load_projects_page_config() -> ProjectsPageConfig:
    """Load metadata from content/pages/projects/index.md to drive the Projects tab header."""

    if not PROJECTS_INDEX_PATH.exists():
        return ProjectsPageConfig(title="Projects")

    meta, _ = parse_frontmatter(PROJECTS_INDEX_PATH)

    page_title = meta.get("title", "Projects")

    hero_title: Optional[str] = None
    hero_subtitle: Optional[str] = None
    for section in meta.get("topSections", []):
        if isinstance(section, dict) and section.get("type") == "HeroSection":
            hero_title = section.get("title") or hero_title
            hero_subtitle = section.get("subtitle") or hero_subtitle
            break

    return ProjectsPageConfig(
        title=page_title,
        hero_title=hero_title,
        hero_subtitle=hero_subtitle,
    )


def load_info_page() -> InfoPageContent:
    """Load key content from content/pages/info.md (about page)."""

    if not INFO_PAGE_PATH.exists():
        return InfoPageContent(
            title="Info",
            hero_text=None,
            skills=[],
            contact_markdown=None,
            experience_markdown=None,
            education_markdown=None,
        )

    meta, _ = parse_frontmatter(INFO_PAGE_PATH)

    title = meta.get("title", "Info")

    hero_text: Optional[str] = None
    skills: List[str] = []
    contact_markdown: Optional[str] = None
    experience_markdown: Optional[str] = None
    education_markdown: Optional[str] = None

    for section in meta.get("sections", []):
        if not isinstance(section, dict):
            continue

        section_type = section.get("type")

        if section_type == "HeroSection" and not hero_text:
            hero_text = section.get("text")

        elif section_type == "LabelsSection" and not skills:
            for item in section.get("items", []):
                if isinstance(item, dict) and item.get("type") == "Label":
                    label = item.get("label")
                    if label:
                        skills.append(label)

        elif section_type == "TextSection" and not contact_markdown:
            subtitle = (section.get("subtitle") or "").lower()
            if "contact" in subtitle:
                contact_markdown = section.get("text")

        elif section_type == "FeaturedItemsSection":
            for item in section.get("items", []):
                if not isinstance(item, dict):
                    continue
                subtitle = (item.get("subtitle") or "").lower()
                text_val = item.get("text")
                if not text_val:
                    continue
                if "experience" in subtitle and not experience_markdown:
                    experience_markdown = text_val
                elif "education" in subtitle and not education_markdown:
                    education_markdown = text_val

    return InfoPageContent(
        title=title,
        hero_text=hero_text,
        skills=skills,
        contact_markdown=contact_markdown,
        experience_markdown=experience_markdown,
        education_markdown=education_markdown,
    )


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


def split_experience_sections(markdown_text: str) -> List[str]:
    """Split the 'Experience' markdown block into smaller sections.

    We treat any line that looks like a markdown heading in the form
    **Some Title** as the start of a new section, and group following
    bullet points with that heading.
    """

    sections: List[str] = []
    current: List[str] = []

    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        if line.startswith("**") and line.endswith("**"):
            # Start a new section when we hit a bold heading
            if current:
                sections.append("\n".join(current).strip())
            current = [line]  # Start new section with the heading
        elif line.strip() == "" and not current:
            # Skip leading blank lines between sections
            continue
        else:
            current.append(line)

    if current:
        sections.append("\n".join(current).strip())

    return [s for s in sections if s]


def render_project_card(project: Project) -> None:
    """Render a single project card inside a column."""

    if project.image_path and project.image_path.exists():
        # Let Streamlit size the image to the column automatically (avoid deprecated use_column_width)
        st.image(str(project.image_path))

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
    # Load content from existing Markdown pages
    home_hero = load_home_hero()
    projects_page = load_projects_page_config()
    info_page = load_info_page()

    # Use the home hero title as the browser/tab title
    st.set_page_config(
        page_title=home_hero.title,
        page_icon="SL",
        layout="wide",
    )

    # Simple navigation similar to the original site header
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Info"], index=0)

    if page == "Home":
        # Use the hero title/subtitle from content/pages/index.md
        st.title(home_hero.title)
        if home_hero.subtitle:
            st.write(home_hero.subtitle)

        projects = load_projects()

        if not projects:
            st.info("No projects found in `content/pages/projects`. Add some .md files to get started.")
        else:
            total = len(projects)
            visible_count = 3 if total >= 3 else total

            # Initialize the carousel index in session state
            if "carousel_index" not in st.session_state:
                st.session_state.carousel_index = 0

            # Navigation controls for the carousel
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

    elif page == "Info":
        st.title(info_page.title)

        if info_page.hero_text:
            st.markdown(info_page.hero_text)

        if info_page.skills:
            st.subheader("Technical Skills")
            st.write(", ".join(info_page.skills))

        if info_page.contact_markdown:
            st.subheader("Contact")
            st.markdown(info_page.contact_markdown)

        if info_page.experience_markdown:
            st.subheader("Experience")
            exp_sections = split_experience_sections(info_page.experience_markdown)
            if exp_sections:
                cols = st.columns(2)
                for idx, section in enumerate(exp_sections):
                    with cols[idx % 2]:
                        # Render each experience entry in its own "box"
                        st.markdown(
                            "<div style='border: 1px solid #444; border-radius: 8px; padding: 12px; margin-bottom: 12px;'>",
                            unsafe_allow_html=True,
                        )
                        st.markdown(section)
                        st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown(info_page.experience_markdown)

        if info_page.education_markdown:
            st.subheader("Education")
            st.markdown(info_page.education_markdown)


if __name__ == "__main__":
    main()
