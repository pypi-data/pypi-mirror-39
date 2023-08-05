# rpc_component

## Component management

#### Register components

```
cd rpc-metadata
component --releases-dir=. add --component-name rpc-product-1 --repo-url https://github.com/mattt416/rpc-product-1
component --releases-dir=. add --component-name rpc-component-1 --repo-url https://github.com/mattt416/rpc-component-1
component --releases-dir=. add --component-name rpc-component-2 --repo-url https://github.com/mattt416/rpc-component-2
```

#### Add dependencies to rpc-product-1

```
cd rpc-product-1
component dependency set-dependency --name rpc-component-1 --constraint "version<r2.0.0"
component dependency set-dependency --name rpc-component-2 --constraint "version<r2.0.0"
```

#### Create dependent component releases

```
cd rpc-metadata
component --releases-dir=. release --component-name rpc-component-1 add --version r1.0.0 --sha 5773026bea0bd72f8920b7e4f0e13e88b368cd55 --series-name master
component --releases-dir=. release --component-name rpc-component-2 add --version r1.0.0 --sha 540464d96be5cbbdf1cf07ae5457dd57b159c110 --series-name master
```

#### Specify dependency requirements

```
cd rpc-product-1
component --releases-dir=../rpc-metadata dependency update-requirements
```

#### Create remaining component release

```
cd rpc-metadata
component --releases-dir=. release --component-name rpc-product-1 add --version r1.0.0 --sha e1d1b2348d9eaae3e5a2217372f97a5144b63355 --series-name master
```

#### Add a component artefact store

```
cd rpc-metadata
component --releases-dir . artifact-store --component-name rpc-product-1 add --name release-artifacts --type file --public-url https://example.com/ --description 'rpc-product-1 release artefacts'
```

## Querying Components

#### Verify the addition of release between <sha1> and <sha2> is valid

```
cd rpc-metadata
component --releases-dir . compare --from <sha1> --to <sha2> --verify release
```

#### Display the predecessor of a given release

```
cd rpc-metadata
component --releases-dir . release --component-name rpc-product-1 get --version r1.0.0 --pred
```

#### Display components that are dependent

```
cd rpc-product-1
component --releases-dir=../rpc-metadata dependents --component-name rpc-product-1
```

#### Verify and get component metadata

```
component metadata get
```

#### Display a component artefact store

```
cd rpc-metadata
component --releases-dir . artifact-store --component-name rpc-product-1 get --name release-artifacts
```
