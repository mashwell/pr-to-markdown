import streamlit as st
import re
from github import Github
from datetime import datetime

st.title("GitHub PR to Markdown Converter")

st.markdown(
    """
    This app fetches a GitHub pull request (including its description, comments, reviews, and file changes)
    and converts it into a Markdown summary. You can then copy the markdown content or download it as a file.
    """
)

# Ask for a GitHub token (optional, but recommended to avoid rate-limiting)
token = st.text_input("GitHub Token (optional)", type="password")

# Input for the GitHub PR URL
pr_url = st.text_input(
    "Enter the GitHub PR URL",
    placeholder="https://github.com/owner/repo/pull/123",
)

if pr_url:
    # Parse the URL to extract owner, repository name, and PR number.
    pattern = r"github\.com/([^/]+)/([^/]+)/pull/(\d+)"
    match = re.search(pattern, pr_url)
    if not match:
        st.error(
            "Invalid PR URL format. Please use a URL like `https://github.com/owner/repo/pull/123`"
        )
    else:
        owner, repo_name, pr_number_str = match.groups()
        pr_number = int(pr_number_str)
        st.info(f"Fetching PR #{pr_number} from **{owner}/{repo_name}** ...")

        try:
            # Authenticate with GitHub using the provided token, if any.
            g = Github(token) if token else Github()
            repo = g.get_repo(f"{owner}/{repo_name}")
            pr = repo.get_pull(pr_number)

            # Build the Markdown content.
            md_lines = []

            # PR Title and basic info.
            md_lines.append(f"# {pr.title}\n")
            md_lines.append(f"**Author:** {pr.user.login}  ")
            md_lines.append(
                f"**Created:** {pr.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            )

            # PR Description.
            md_lines.append("## Description\n")
            if pr.body:
                md_lines.append(pr.body + "\n")
            else:
                md_lines.append("_No description provided._\n")

            # Issue Comments (the conversation comments on the PR as an issue)
            md_lines.append("## Issue Comments\n")
            issue_comments = list(pr.get_issue_comments())
            if issue_comments:
                for comment in issue_comments:
                    md_lines.append(
                        f"### Comment by {comment.user.login} on {comment.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                    )
                    md_lines.append(comment.body + "\n")
            else:
                md_lines.append("_No issue comments._\n")

            # Inline Review Comments (comments on specific code lines)
            md_lines.append("## Inline Review Comments\n")
            review_comments = list(pr.get_review_comments())
            if review_comments:
                for rc in review_comments:
                    # Some inline comments may not have a `position` (if the diff context is not available)
                    position = f" at line {rc.position}" if rc.position else ""
                    md_lines.append(
                        f"### Comment by {rc.user.login} on {rc.created_at.strftime('%Y-%m-%d %H:%M:%S')} in `{rc.path}`{position}\n"
                    )
                    md_lines.append(rc.body + "\n")
            else:
                md_lines.append("_No inline review comments._\n")

            # Reviews (the overall review summaries provided by reviewers)
            md_lines.append("## Reviews\n")
            reviews = list(pr.get_reviews())
            if reviews:
                # It’s possible that a reviewer has submitted multiple reviews,
                # so we simply list them in order.
                for review in reviews:
                    submitted = (
                        review.submitted_at.strftime("%Y-%m-%d %H:%M:%S")
                        if review.submitted_at
                        else "N/A"
                    )
                    md_lines.append(
                        f"### Review by {review.user.login} on {submitted}\n"
                    )
                    md_lines.append(f"**State:** {review.state}\n")
                    if review.body:
                        md_lines.append(review.body + "\n")
            else:
                md_lines.append("_No reviews provided._\n")

            # File Changes (contents of the PR)
            md_lines.append("## File Changes\n")
            files = list(pr.get_files())
            if files:
                for file in files:
                    md_lines.append(f"### {file.filename}\n")
                    if file.patch:
                        md_lines.append("```diff")
                        md_lines.append(file.patch)
                        md_lines.append("```")
                    else:
                        md_lines.append("_No diff available for this file._\n")
            else:
                md_lines.append("_No file changes available._\n")

            # Combine all lines into a single Markdown string.
            md_content = "\n".join(md_lines)

            st.subheader("Markdown Output")
            st.text_area("Markdown Content", md_content, height=400)

            # Provide a download button for the Markdown content.
            st.download_button(
                "Download Markdown",
                md_content,
                file_name=f"PR_{pr_number}.md",
                mime="text/markdown",
            )

        except Exception as e:
            st.error(f"An error occurred while fetching the PR: {e}")
