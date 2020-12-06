# clustogram
Transforms a IaC k8s description (in the form of k8s .yaml and Terraform .hcls) into object diagram

## Usage
...

## Note on abstraction
This product may introduce some abstraction, example: given deployment and a matching service - technically services point at pods created by replication controlers, created by deployments. But in our graphs the service will point directly at the deployment. Which at conceptual level makes sense.

## Dev

### Prerequisites
- [nix](https://nixos.org/nix/manual/#chap-installation)
- `direnv` (`nix-env -iA nixpkgs.direnv`)
- [configured direnv shell hook ](https://direnv.net/docs/hook.html)
- some form of `make` (`nix-env -iA nixpkgs.gnumake`)

Hint: if something doesn't work because of missing package please add the package to `default.nix` instead of installing on your computer. Why solve the problem for one if you can solve the problem for all? ;)
### Structure
- `ulmz` - UML documentation
- `cli` - parses .hcl, .yamls into a stream of normalized k8s objects
- `graph` - finds connections between k8s objects in a loose collection
- `ui`- displays the connections

### One-time setup (this directory only)
```
make init
```

### Everything - (in each of the directories)
```
make help
```
