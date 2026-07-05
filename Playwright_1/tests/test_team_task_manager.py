import re

from playwright.sync_api import Page, expect


APP_URL = "https://team-task-manager-dusky-seven.vercel.app/"


def open_task_manager(page: Page) -> None:
    page.goto(APP_URL)
    expect(
        page.get_by_role("button", name=re.compile("add task|new task", re.IGNORECASE))
    ).to_be_visible()


def task_card(page: Page, task_name: str):
    return page.locator("[data-testid='task-card']").filter(has_text=task_name)


def create_task(
    page: Page,
    title: str = "Prepare sprint report",
    description: str = "Create weekly sprint status report",
    assignee: str = "Alex",
    priority: str = "High",
) -> None:
    page.get_by_role("button", name=re.compile("add task|new task", re.IGNORECASE)).click()
    page.get_by_label(re.compile("task title|title", re.IGNORECASE)).fill(title)
    page.get_by_label(re.compile("description", re.IGNORECASE)).fill(description)
    page.get_by_label(re.compile("assignee|assigned to", re.IGNORECASE)).select_option(
        label=assignee
    )
    page.get_by_label(re.compile("priority", re.IGNORECASE)).select_option(label=priority)
    page.get_by_role("button", name=re.compile("save|create", re.IGNORECASE)).click()

    expect(page.get_by_text(title)).to_be_visible()


def test_user_can_create_new_task(page: Page) -> None:
    open_task_manager(page)

    create_task(page)

    expect(page.get_by_text("Prepare sprint report")).to_be_visible()
    expect(page.get_by_text("Alex")).to_be_visible()
    expect(page.get_by_text("High")).to_be_visible()


def test_user_can_mark_task_as_completed(page: Page) -> None:
    open_task_manager(page)
    create_task(page, title="Complete sprint checklist")

    task = task_card(page, "Complete sprint checklist")
    task.get_by_role("checkbox").check()

    expect(task).to_have_class(re.compile("completed|done", re.IGNORECASE))


def test_user_can_edit_existing_task(page: Page) -> None:
    open_task_manager(page)
    create_task(page, title="Prepare sprint report")

    task = task_card(page, "Prepare sprint report")
    task.get_by_role("button", name=re.compile("edit", re.IGNORECASE)).click()

    page.get_by_label(re.compile("task title|title", re.IGNORECASE)).fill(
        "Prepare final sprint report"
    )
    page.get_by_role("button", name=re.compile("update|save", re.IGNORECASE)).click()

    expect(page.get_by_text("Prepare final sprint report")).to_be_visible()
    expect(page.get_by_text("Prepare sprint report")).not_to_be_visible()


def test_user_can_delete_task(page: Page) -> None:
    open_task_manager(page)
    create_task(page, title="Delete old task")

    task = task_card(page, "Delete old task")
    task.get_by_role("button", name=re.compile("delete|remove", re.IGNORECASE)).click()
    page.get_by_role("button", name=re.compile("confirm|yes|delete", re.IGNORECASE)).click()

    expect(page.get_by_text("Delete old task")).not_to_be_visible()


def test_user_can_filter_tasks_by_status(page: Page) -> None:
    open_task_manager(page)
    create_task(page, title="Done task")

    task = task_card(page, "Done task")
    task.get_by_role("checkbox").check()
    page.get_by_role("button", name=re.compile("completed|done", re.IGNORECASE)).click()

    completed_tasks = page.locator("[data-testid='task-card']")
    expect(completed_tasks.first()).to_contain_text("Done task")


def test_validation_message_appears_when_task_title_is_empty(page: Page) -> None:
    open_task_manager(page)

    page.get_by_role("button", name=re.compile("add task|new task", re.IGNORECASE)).click()
    page.get_by_label(re.compile("task title|title", re.IGNORECASE)).fill("")
    page.get_by_role("button", name=re.compile("save|create", re.IGNORECASE)).click()

    expect(
        page.get_by_text(re.compile("task title is required|title is required", re.IGNORECASE))
    ).to_be_visible()
