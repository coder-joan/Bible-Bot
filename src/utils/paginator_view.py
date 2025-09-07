import discord

from typing import List
from collections import deque

class PaginatorView(discord.ui.View):
    def __init__(self, embeds: List[discord.Embed]) -> None:
        super().__init__(timeout=None)
        self.embeds = deque(embeds)
        self.current_page = 1
        self.total_pages = len(embeds)

        if self.total_pages == 1:
            self.previous_page.disabled = True
            self.next_page.disabled = True

    def update_footer(self) -> discord.Embed:
        embed = self.embeds[0]
        embed.set_footer(text=f"Page {self.current_page} of {self.total_pages}")
        return embed

    async def change_page(self, interaction: discord.Interaction, direction: int):
        self.embeds.rotate(direction)
        self.current_page = (self.current_page - direction - 1) % self.total_pages + 1
        await interaction.response.edit_message(embed=self.update_footer())

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="⬅️")
    async def previous_page(self, interaction: discord.Interaction, _):
        await self.change_page(interaction, 1)

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="➡️")
    async def next_page(self, interaction: discord.Interaction, _):
        await self.change_page(interaction, -1)

    @property
    def initial(self) -> discord.Embed:
        return self.update_footer()