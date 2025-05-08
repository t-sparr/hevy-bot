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

## Features

- **Smart Discovery**: Finds users from the Discover feed who are actively commenting or liking others.
- **Automated Following**: Follows users based on engagement criteria.
- **Unfollowing Logic**: Removes users who are inactive or don’t follow back within a set time.
- **Workout Liking**: Likes recent workouts from discovered users to boost interaction.
- **Token Health Monitoring**: Confirms valid session with the Hevy API.
- **Discord Webhooks**: Sends status summaries and errors directly to Discord.

---

## How it Works

The bot is orchestrated through `hevy_bot.py` and works in five key stages, using a combination of **GET** and **POST** requests to interact with the Hevy API:

### 1. **Get Current Network**
- `GET /following/{username}` — gets who you follow
- `GET /followers_paged/{username}` — gets your followers  
Used to identify new users and monitor engagement status.

### 2. **Discover Users to Follow**
- `GET /discover_feed_workouts_paged` — scrapes the discover feed
- `GET /workout_likes/{workout_id}` — pulls likers of a workout  
Users are chosen based on commenting and liking behavior. Already-followed and whitelisted users are skipped.

### 3. **Follow Users**
- `POST /follow` with `{ "username": "target_user" }`  
New users are followed and logged with a timestamp. Stops automatically if rate-limited or blocked.

### 4. **Unfollow Users**
- `POST /unfollow` with `{ "username": "target_user" }`  
Users are unfollowed if:
  - They haven’t followed back after `N` days
  - They’ve been inactive for `X` days
  - They’re not on the whitelist

### 5. **Like Workouts**
- `GET /user_workouts_paged?username=target&limit=1` — fetches latest workout
- `POST /workout/like/{workout_id}` — likes the workout  
Each like is logged and checked to avoid repetition.

### 6. **Send Discord Summary**
- `POST` to a configured Discord webhook  
Sends a log of who was followed/unfollowed with optional user mentions for alerts.

All actions are rate-limited with randomized delays to mimic human behavior.

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