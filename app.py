import os
import flet as ft
from assistant import Assistant

class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type

class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment="start"
        self.controls=[
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.colors.WHITE,
                    bgcolor=self.get_avatar_color(message.user_name),
                ),
                ft.Column(
                    [
                        ft.Text(message.user_name, weight="bold"),
                        ft.Text(message.text, selectable=True, width=500),
                    ],
                    tight=True,
                    spacing=5,
                ),
            ]

    def get_initials(self, user_name: str):
        if user_name == None:
            user_name = "No user "
        return user_name[:1].capitalize()

    def get_avatar_color(self, user_name: str):
        colors_lookup = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colors_lookup[hash(user_name) % len(colors_lookup)]

def main(page: ft.Page):
    # page.horizontal_alignment = "stretch"
    page.title = "The scuttling crab"
    page.theme_mode = "dark"
    page.fonts = {
        "organical": "fonts/organical.ttf"
    }

    # creating the object of Assistant class
    assistant = Assistant()

    def join_chat_click(e):
        if not join_user_name.value:
            join_user_name.error_text = "We need to know our names first!"
            join_user_name.update()
        else:
            page.session.set("user_name", join_user_name.value)
            page.dialog.open = False
            new_message.prefix = ft.Text(f"{join_user_name.value}: ")
            page.pubsub.send_all(Message(user_name=join_user_name.value, text=f"{join_user_name.value} has joined the chat.", message_type="login_message"))
            page.update()

    def send_message_click(e):
        if new_message.value != "":
            # sending the user input
            page.pubsub.send_all(Message(page.session.get("user_name"), new_message.value, message_type="chat_message"))
            
            # asking user to wait till we get our response
            page.pubsub.send_all(Message(user_name="Robbert the crab", text="AI crab is getting the response for you...", message_type="login_message"))

            # fetching the SmartGuru AI response
            ai_response = assistant.Response(str(new_message.value))
            page.pubsub.send_all(Message("AI crab", str(ai_response).lstrip(), message_type="chat_message"))

            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    # A dialog asking for a user display name
    join_user_name = ft.TextField(
        label="Tell me your name...",
        autofocus=True,
        on_submit=join_chat_click,
    )
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([join_user_name], width=300, height=70, tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=join_chat_click)],
        actions_alignment="end",
    )

    # Chat messages
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    # A new message entry form
    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        border_radius=20,
        on_submit=send_message_click,
        border_color=ft.colors.BLUE
    )

    # Add everything to the page
    page.add(
        ft.Row([ft.Text("AI Crab", font_family="organical", style="headlineLarge", color="blue")], alignment="center"),
        ft.Container(
            content=chat,
            border=ft.border.all(2, ft.colors.BLUE),
            border_radius=20,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=send_message_click,
                    icon_color=ft.colors.BLUE
                ),
            ]
        ),
    )


# ft.app(port=9000, target=main, view=ft.WEB_BROWSER, assets_dir="assets")
ft.app(target=main) 