# HEVY-BOT

This is a modular Python automation bot for [Hevy](https://www.hevyapp.com/), designed to boost community engagement by automatically liking workouts, following active users, and unfollowing inactive or unreciprocated follows.

> This is a **showcase version**. Sensitive tokens, credentials, and internal datasets have been removed.

---

## Features

- **Smart Discovery**: Finds users from the Discover feed who are actively commenting or liking others.
- **Automated Following**: Follows users based on engagement criteria.
- **Unfollowing Logic**: Removes users who are inactive or don’t follow back within a set time.
- **Workout Liking**: Likes recent workouts from discovered users to boost interaction.
- **Token Health Monitoring**: Confirms valid session with the Hevy API.
- **Discord Webhooks**: Sends status summaries and errors directly to Discord.

---

## How it Works

The bot runs in a sequence via `hevy_bot.py`:

1. **Checks your current followers/following**
2. **Collects potential users to follow** from likes/comments
3. **Follows them**, respecting past follows/unfollows
4. **Unfollows users** that:
   - Don’t follow back after `X` days
   - Are inactive for `Y` days
5. **Sends a summary** to Discord

Everything is rate-limited and safely spaced using randomized delays.

---

## Discord Log
**----------------- Session Summary -----------------**

✅ **Followed (30):**
@sergiototti  
@vikingfoxx  
@c187  
@lachy_coops  
@its_darpan  
@arvindsharma  
@zeros11  
@sara_no_h  
@mircea  
@rhynoone  
@abedkh  
@mauoliver  
@nnkumar  
@pt_k  
@camsza02  
@liu34w  
@alex567890  
@yingx  
@mikerosoftexcels  
@tmckinneyusa  
@thejeets89  
@slavey17  
@g_bs1  
@jb320qa  
@ache_alpha  
@warriorinagarden1  
@b_davis616  
@gemma595  
@kali_will  
@diogenescordeiro  

🚫 **Unfollowed (16):**
@christofer_monteiro — *Hasn't followed back after 3+ days*  
@geogirl — *Hasn't followed back after 3+ days*  
@hirocosm — *Hasn't followed back after 3+ days*  
@nanananananashi — *Hasn't followed back after 3+ days*  
@ninjapastor — *Inactive for 14+ days*  
@capetown — *Hasn't followed back after 3+ days*  
@menze03 — *Hasn't followed back after 3+ days*  
@ronniehersh — *Hasn't followed back after 3+ days*  
@mikebloos — *Hasn't followed back after 3+ days*  
@torontojames — *Hasn't followed back after 3+ days*  
@julz — *Hasn't followed back after 3+ days*  
@bengriffiths — *Hasn't followed back after 3+ days*  
@eblifting — *Hasn't followed back after 3+ days*  
@theviking_nico — *Hasn't followed back after 3+ days*  
@smartchoicecz — *Hasn't followed back after 3+ days*  
@board817 — *Hasn't followed back after 3+ days*  