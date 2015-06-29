import os
import sys
import vlc
import pygame
 
def play_vid(video):
    # Enable in Windows to use directx renderer instead of windib
    if sys.platform == "win32":
        os.environ["SDL_VIDEODRIVER"] = "directx"
 
    print "Using %s renderer" % pygame.display.get_driver()
    print 'Playing: %s' % video
 
    # Get path to movie specified as command line argument
    movie = os.path.expanduser(video)
    # Check if movie is accessible
    if not os.access(movie, os.R_OK):
        print('Error: %s file not readable' % movie)
        sys.exit(1)
 
    # Create instance of VLC and create reference to movie.
    vlcInstance = vlc.Instance()
    media = vlcInstance.media_new(movie)
 
    # Create new instance of vlc player
    player = vlcInstance.media_player_new()
 
    # Pass pygame window id to vlc player, so it can render its contents there.
    win_id = pygame.display.get_wm_info()['window']
    if sys.platform == "linux2": # for Linux using the X Server
        player.set_xwindow(win_id)
    elif sys.platform == "win32": # for Windows
        player.set_hwnd(win_id)
    elif sys.platform == "darwin": # for MacOS
        player.set_agl(win_id)
 
    # Load movie into vlc player instance
    player.set_media(media)
 
    # Quit pygame mixer to allow vlc full access to audio device (REINIT AFTER MOVIE PLAYBACK IS FINISHED!)
    pygame.mixer.quit()
 
    # Start movie playback
    player.play()
 
    while player.get_state() != vlc.State.Ended and player.get_state() != vlc.State.Stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(2)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.stop()
                print "OMG keydown!"
            if event.type == pygame.MOUSEBUTTONDOWN:
                print "we got a mouse button down!"
if __name__=='__main__':
    play_vid('Intro.mp4')