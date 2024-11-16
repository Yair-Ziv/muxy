import os
import yaml
import sys
import subprocess

# Path to the configuration file
CONFIG_PATH = os.path.expanduser('~/.config/tmuxInitializer/config.yaml')

def load_config(path):
    '''Load configuration from the YAML file.'''
    with open(path, 'r') as file:
        return yaml.safe_load(file)

def attach_to_session(session_name):
    subprocess.run(['tmux', 'attach-session', '-t', session_name])

def create_tmux_session(config, session_name):
    '''Create tmux session based on the configuration.'''
    session = config[session_name]
    windows = session['windows']

    # Create the tmux session
    subprocess.run(['tmux', 'new-session', '-d', '-s', session_name])

    for i, window in enumerate(windows):
        window_name = window['name']
        command = window.get('command')

        if i == 0:
            subprocess.run(['tmux', 'rename-window', '-t', f'{session_name}:{i}', window_name])
        else:
            subprocess.run(['tmux', 'new-window', '-t', session_name, '-n', window_name])
        
        if command:
            subprocess.run(['tmux', 'send-keys', '-t', f'{session_name}:{i}', command, 'C-m'])

    # Attach to the session
    attach_to_session(session_name)

def tmux_session_exists():
    # TODO: Implement
    return False

def main():
    print(sys.argv)
    if not os.path.exists(CONFIG_PATH):
        print(f'Configuration file not found at {CONFIG_PATH}')
        return
    if len(sys.argv) != 2:
        print("Missing argumant session_name")
        return 1
    
    session_name = sys.argv[1]
    if (tmux_session_exists()):
        attach_to_session(session_name)

    config = load_config(CONFIG_PATH)
    create_tmux_session(config, session_name)

if __name__ == '__main__':
    main()
