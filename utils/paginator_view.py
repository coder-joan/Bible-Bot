import discord
from typing import List, Optional

class PaginatorView(discord.ui.View):
    def __init__(
            self, 
            embeds: List[discord.Embed], 
            bible_translation: Optional[str] = None, 
            timeout: int = 300
        ) -> None:

        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.bible_translation = bible_translation
        self.current_page = 0
        self.total_pages = len(embeds)
        self.message: Optional[discord.Message] = None

        if self.total_pages == 1:
            self.previous_page.disabled = True
            self.next_page.disabled = True

    def update_footer(self) -> discord.Embed:
        embed = self.embeds[self.current_page]
        page_info = f"Page {self.current_page + 1} of {self.total_pages}"

        if self.bible_translation:
            embed.set_footer(text=f"{page_info} • {self.bible_translation}")
        else:
            embed.set_footer(text=page_info)
        return embed

    async def change_page(self, interaction: discord.Interaction, direction: int):
        self.current_page = (self.current_page + direction) % self.total_pages
        await interaction.response.edit_message(embed=self.update_footer(), view=self)

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="⬅️")
    async def previous_page(self, interaction: discord.Interaction, _):
        await self.change_page(interaction, -1)

    @discord.ui.button(style=discord.ButtonStyle.secondary, emoji="➡️")
    async def next_page(self, interaction: discord.Interaction, _):
        await self.change_page(interaction, 1)

    @property
    def initial(self) -> discord.Embed:
        return self.update_footer()