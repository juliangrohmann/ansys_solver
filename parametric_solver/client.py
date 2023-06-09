import requests
import time


class SolverClient:
    """
    A web-client that gets samples on-demand from its server counterpart (SolverServer),
    solves, and stores the solution.

    For use with the SLURM compute cluster.
    """
    def __init__(self, server_url, solver):
        """
        Parameters
        ----------
        server_url: str
            The server's URL (i.e. IP address or hostname).

        solver: <? extends ParametricSolver>
            Any suitable parametric solver that implements the ParametricSolver base class and will be used for solving.
        """
        self._server_url = server_url
        self._solver = solver

    def _get_sample(self, retry_interval=10):
        fail_count = 0

        while True:
            try:
                request = 'http://' + self._server_url + '/sample'
                print(f"Requesting new sample from {request} ...")
                response = requests.get(request, timeout=5)
                print(response)

                if response.status_code == 200:
                    sample = tuple(response.json())
                    print(f"Received sample {sample}")
                    return sample
                elif response.status_code == 404:
                    print("Solved all samples. Exiting ...")
                    return None
                else:
                    raise Exception(f"Error: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Exception: {e}")
                fail_count += 1
                if fail_count >= 10:
                    print("Too many failed attempts. Exiting ...")
                    return None

                print(f"Server not available (fail count = {fail_count}). Retrying in", retry_interval, "seconds ...")
                time.sleep(retry_interval)

    def run(self):
        """
        Launches the client.

        Notes
        -----
        When the current sample is solved, or when the client is first initialized,
        it will attempt to get a new sample from the solver.

        Only one sample is retrieved at a time and solved immediately.

        If the server cannot be reached, the client will time out for 10 seconds and re-attempt,
        up to a maximum of 10 times.

        If the server responds with 404, all samples are solved and the client will terminate.
        """
        next_sample = self._get_sample()
        while next_sample:
            print(f"Solving for sample {next_sample} ...")
            self._solver.add_sample(*next_sample)
            self._solver.solve(verbose=True)
            print("Solve completed.")
            next_sample = self._get_sample()
