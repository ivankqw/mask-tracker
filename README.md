## Motivation
Given the current COVID-19 situation, it is of utmost importance that citizens are wearing masks while outdoors at all times, to effectively reduce the spread of COVID-19. To combat the spread of COVID-19, the Singapore government has been issuing its citizens reusable masks for their daily use. Along with each mask comes a note stating the maximum number of mask washes before the mask becomes less effective in preventing the spread of infectious diseases. It is difficult, however, to keep track of the number of times people use their reusable masks, and this problem is worsened when people have multiple masks. **This creates a problem when people over-wash their masks and wear masks that are less effective while outdoors. This puts them at a greater risk of contracting COVID-19. We have thus come up with a simple telegram bot to allow users to easily keep track of these numbers.**

## Commands
`/add` mask_name max_washes to start tracking a new mask

`/remove` to stop tracking a mask

`/wash` after you have washed the mask.

`/help` for information on additional commands

###Additional Commands 
`/editname` old_name new_name to change the name of your mask.

`/editcurrent` mask_name current_washes can be used to change the number of times the mask has been washed.

`/editmax` mask_name max_washes to change the max number of washes for the mask

## How we built it
Using [Telegram API](https://core.telegram.org/bots/api), we generated a token from **@BotFather**. For the code, it is mostly based on CommandHandler, Message Handler, ReplyKeyboardMarkup. 
