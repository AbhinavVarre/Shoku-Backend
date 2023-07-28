# Shoku-Backend

## Using the API:

In order to use the API, once you've [launched](#launch) it, go to: http://127.0.0.1:5001/

You can see the routes available in the server.js file. For instance, try going to: http://127.0.0.1:5001/api

Happy Coding!

## First time startup: 

**All of the following commands are run in your terminal. After installing Yarn, every command must be run in the Shoku-Backend Directory.**


After locally cloning the repo, in your terminal, first run:

```
yarn --version
```
If this commmand returns something similar to below, you must install yarn first. Otherwise, you may skip the Installing Yarn step.

```
command not found: yarn
```

### Installing Yarn:

**Yarn is the package manager we use instead of npm - it downloads packages much faster.**

Anytime you watch a tutorial that uses npm, you want to use yarn instead. Check [this link](https://www.digitalocean.com/community/tutorials/nodejs-npm-yarn-cheatsheet) for mappings between npm commands to yarn commands.
For instance, instead of running <em>npm i some-package</em> you would run <em>yarn add some-package</em>

To install yarn, run this command:

```
sudo npm i -g yarn
```
You will be prompted for your computer password. Enter it and hit enter.
<br/>
<br/>

### Installing Packages:

When you first open the code files, you will see many errors. This is because the necessary libraries have not been downloaded.


**You must open a terminal in the directory of the Shoku-Backend Directory for the remaining terminal commands.**


To download all the libraries you need, run:

```
yarn
```

<h3 id="launch">Launching App</h3>

This is the command you must run in your terminal to launch the application every time you would like to launch.

**To launch the application, run:** 

```
yarn dev
```

When running this command for the first time, you might be prompted to install certain packages. **Enter y to accept**

**The console should have a message that states "server started" if the server launches successfully.**
