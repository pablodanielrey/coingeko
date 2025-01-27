#!/bin/bash
docker run --rm -ti -e COIN_IDS="ripple,stellar,cardano,solana,hedera-hashgraph,ethereum,radium" -p 1280:8080 coingeko-server 