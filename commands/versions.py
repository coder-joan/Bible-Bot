import discord
from discord import app_commands

from config.colors import STANDARD_COLOR
from utils.paginator_view import PaginatorView

@app_commands.command(name="versions", description="Available Bible translations")
async def versions(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    description = [
        f'Below you can find a list of all available Bible translations that you can use '
         'in the bot commands:\n\n'

         '**Afrikaans:**\n\n'

         '`AFRI` - Afrikaans (1953)\n\n'

         '**Arabic:**\n\n'

         '`SVD` - Smith and van Dyck (1865)\n'
         '`NAV` - New Arabic Version (1997)\n\n'

         '**Chinese:**\n\n'

         '`CHIUNS` - Chinese Union Simplified (1919)\n'
         '`CHIUN` - Chinese Union Traditional (1919)\n'
         '`CHISB` - Sīgāo Běn (1960)',

        f'Below you can find a list of all available Bible translations that you can use '
         'in the bot commands:\n\n'

         '`NCVS` - Chinese New Version Simplified (2010)\n\n'

         '**English:**\n\n'

         '`KJV` - King James Version (1769)\n'
         '`ASV` - American Standard Version (1901)\n'
         '`RSV` - Revised Standard Version (1952)\n'
         '`NKJV` - New King James Version (1982)\n'
         '`NET` - NET Bible (1996)\n'
         '`AKJV` - American King James Version (1999)\n'
         '`UKJV` - Updated King James Version (2000)\n'
         '`ESV` - English Standard Version (2001)\n'
         '`WEB` - World English Bible (2006)\n'
         '`NIV` - New International Version (2011)',

        f'Below you can find a list of all available Bible translations that you can use '
         'in the bot commands:\n\n'

         '**French:**\n\n'

         '`FRES` - Bible Louis Segond (1910)\n'
         '`FREC` - La Bible Augustin Crampon (1923)\n'
         '`OSTER` - Ostervald (1996)\n\n'

         '**German:**\n\n'

         '`LUTH` - Luther Bibel (1545)\n'
         '`ELB` - Elberfelder Bibel (1871)\n'
         '`GRUN` - Grünewaldbibel (1924)\n'
         '`SCH` - Schlachter Bibel (2000)',

        f'Below you can find a list of all available Bible translations that you can use '
         'in the bot commands:\n\n'

         '**Greek:**\n\n'

         '`LXX` - Septuagint\n'
         '`TR` - Textus Receptus (1550)\n'
         '`NE` - Nestle (1904)\n'
         '`BYZ` - Byzantine Text (2013)\n\n'

         '**Hebrew:**\n\n'

         '`ALEP` - Aleppo Codex\n'
         '`WLC` - Westminster Leningrad Codex\n'
         '`HEBM` - Modern Hebrew Bible',

        f'Below you can find a list of all available Bible translations that you can use '
         'in the bot commands:\n\n'

         '**Hindi:**\n\n'

         '`IRV` - Indian Revised Version (2018)\n\n'

         '**Japanese:**\n\n'

         '`BUN` - Japanese Bungo-yaku (1953)\n'
         '`KOU` - Japanese Kougo-yaku (1955)\n\n'

         '**Korean:**\n\n'

         '`KOR` - Korean Bible\n'
         '`KHKJV` - Hangul King James Version',

        f'Below you can find a list of all available Bible translations that you can use '
         'in the bot commands:\n\n'

         '**Latin:**\n\n'

         '`VG` - Vulgate\n\n'

         '**Portuguese:**\n\n'

         '`LIV` - Bíblia Livre\n'
         '`PORA` - Bíblia João Ferreeira DAlmeida (1911)\n'
         '`PORCAP` - Bíblia Sagrada Capuchinhos (2017)\n\n'

         '**Russian:**\n\n'

         '`SYN` - Russian Synodal Bible (1876)',

        f'Below you can find a list of all available Bible translations that you can use '
         'in the bot commands:\n\n'

         '**Spanish:**\n\n'

         '`RV` - Reina-Valera (1909)\n\n'

         '**Vietnamese:**\n\n'

         '`NVB` - New Vietnamese Bible (2002)\n'
         '`LCCMN` - Lời Chúa Cho Mọi Người (2007)'
    ]

    embeds = [discord.Embed(title="Available Bible translations", description=desc, color=STANDARD_COLOR) for desc in description]
    view = PaginatorView(embeds)
    
    await interaction.followup.send(embed=view.initial, view=view)