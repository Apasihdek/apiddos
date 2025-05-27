def run_attack(host, port, time, proxy, user_agent):
    return f"HTTP GET flood on {host}:{port} for {time}s using proxy {proxy} and UA {user_agent}"
