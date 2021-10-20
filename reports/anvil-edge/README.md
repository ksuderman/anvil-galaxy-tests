# Automated Tests for Galaxy on Kubernetes Stacks
## Galaxy on GKE deployed via GalaxyKubeMan (AnVIL)
### Deployment Testing
Twice a day, [GalaxyKubeMan (GKM)](https://github.com/galaxyproject/galaxykubeman-helm) is deployed on GKE, mimicking an AnVIL deployment. The purpose of these tests is to provide reasonable confidence that Galaxy is launchable on the AnVIL everyday.

Below is a plot summarizing successful deployments and GKM install times.
<a href="https://htmlpreview.github.io/?https://github.com/anvilproject/galaxy-tests/blob/main/reports/anvil-edge/deployments.html">Click here</a> or on the image for more details.

<a href="https://htmlpreview.github.io/?https://github.com/anvilproject/galaxy-tests/blob/main/reports/anvil-edge/deployments.html"><img src="deployments.svg" /></a>

### Tool Testing
After each successful deployment, automated tool tests are also run against the instance. These serve as an end-to-end-like test for Galaxy, providing confidence that Galaxy is not only launchable but functional. These tests cycle on a weekly basis through the entire suite of tools installed by default on AnVIL, providing reasonable confidence that the tools encountered by most users remain functional, and automating the detection and reporting of tools breaking.

Latest tool tests for each chunk:

<table id="anviltools"><thead><tr><th>Chunk ID</th><th>Tool List</th><th>Latest report</th><th>Previous report</th></tr></thead><tbody><tr><td>1</td><td><a href="https://github.com/anvilproject/galaxy-tests/blob/main/reports/anvil-edge/tool-tests/gxy-auto-10-18-22-12-27-1/tools.yaml">Toolset</a></td><td><a href="https://htmlpreview.github.io/?https://github.com/anvilproject/galaxy-tests/blob/main/reports/anvil-edge/tool-tests/gxy-auto-10-18-22-12-27-1/results.html">Mon Oct 18 22:20:11 2021</a></td><td><a href="N/A">N/A</a></td></tr><tr><td>2</td><td><a href="https://github.com/anvilproject/galaxy-tests/blob/main/reports/anvil-edge/tool-tests/gxy-auto-10-19-10-15-57-1/tools.yaml">Toolset</a></td><td><a href="https://htmlpreview.github.io/?https://github.com/anvilproject/galaxy-tests/blob/main/reports/anvil-edge/tool-tests/gxy-auto-10-19-10-15-57-1/results.html">Tue Oct 19 10:23:27 2021</a></td><td><a href="N/A">N/A</a></td></tr><tr><td>3</td><td><a href="https://github.com/anvilproject/galaxy-tests/blob/main/reports/anvil-edge/tool-tests/gxy-auto-10-19-22-12-31-1/tools.yaml">Toolset</a></td><td><a href="https://htmlpreview.github.io/?https://github.com/anvilproject/galaxy-tests/blob/main/reports/anvil-edge/tool-tests/gxy-auto-10-19-22-12-31-1/results.html">Tue Oct 19 22:21:00 2021</a></td><td><a href="N/A">N/A</a></td></tr><tr><td>4</td><td><a href="https://github.com/anvilproject/galaxy-tests/blob/main/reports/anvil-edge/tool-tests/gxy-auto-10-20-10-15-42-1/tools.yaml">Toolset</a></td><td><a href="https://htmlpreview.github.io/?https://github.com/anvilproject/galaxy-tests/blob/main/reports/anvil-edge/tool-tests/gxy-auto-10-20-10-15-42-1/results.html">Wed Oct 20 10:22:56 2021</a></td><td><a href="N/A">N/A</a></td></tr></tbody></table>
