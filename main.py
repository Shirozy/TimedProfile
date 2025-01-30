# Run on schedule:
import discord_profile_picturer
import schedule
import time

def startPicturer():
    """
    Attempt to update profile picture.
    
    Returns:
        bool: Whether the PFP update was successful or not.
    """
    picturer = discord_profile_picturer.DiscordProfilePicturer()
    try:
        if picturer.update_profile_picture():
            print("Profile picture changed successfully")
            return True
        else:
            print(f"Error updating profile picture: {picturer.get_last_error()}")
            return False
    except Exception as e:
        print(f"An unexpected error occurred while updating profile picture: {e}")
        return False

schedule.every().day.at("08:01").do(startPicturer)
schedule.every().day.at("11:01").do(startPicturer)
schedule.every().day.at("18:01").do(startPicturer)
schedule.every().day.at("22:01").do(startPicturer)

while True:
    schedule.run_pending()
    time.sleep(60)


# -- Example script to run the tool: --

# picturer = discord_profile_picturer.DiscordProfilePicturer()

#     if picturer.update_profile_picture():
#         print("Profile picture changed successfully")
#     else:
#         print("Error updating profile picture")