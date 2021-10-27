import subprocess

# Define some basic commands to operate docker with


def build():
    # Build containers
    subprocess.run(
        f"docker-compose build --no-cache --parallel", shell=True, check=True
    )


def start():
    # Build containers
    subprocess.run(f"docker-compose up -d", shell=True, check=True)


def init():
    build()
    start()


def up():
    # Start services in deamon mode
    subprocess.run(f"docker-compose up -d", shell=True, check=True)


def stop():
    # Stop services
    try:
        subprocess.run(f"docker-compose stop", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Warning: docker-compose stop failed with non zero exit status")


def remove():
    # Remove containers.
    try:
        subprocess.run(f"docker rm -f backend frontend", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("docker rm -f backend frontend -- Failed with non zero exit status")


def status():
    # Get cluster status
    subprocess.run(f"docker ps -a", shell=True, check=True)
