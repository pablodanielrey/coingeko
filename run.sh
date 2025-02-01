#!/bin/bash
docker run --rm -ti -e COIN_IDS="ripple,stellar,cardano,solana,hedera-hashgraph,ethereum,bitcoin,bitcoin-2-0" -p 1280:8080 pablodanielrey/coingeko-server 