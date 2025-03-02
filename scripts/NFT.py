from blockchain import Blockchain
from certificate import Certificate
from block import Block
from timestamp import now
import random
import os


class NFT:
    def __init__(self, token_id, metadata, ownerPublicKey):
        self.token_id = token_id    # Identifiant unique du NFT
        self.metadata = metadata   # données dans le NFT (image,description...)
        self.ownerPublicKey = ownerPublicKey

    def display(self):
        #représentation simple du NFT
        return {
            'token_id': self.token_id,
            'metadata': self.metadata,
            'owner': self.ownerPublicKey[-16:]  # Affichage partiel pour lisibilité
        }
    

class Collection:
    def __init__(self, ownerPublicKey, limit, mintDuration):
        self.ownerPublicKey = ownerPublicKey
        self.limit = limit
        self.mintDuration = mintDuration
        self.mintStart = None  # timestamp début de minting
        self.mintEnd = None    # timestamp de fin
        self.nftRegistry = {}  # ictionnaire token_id -> NFT
        self.nextTokenId = 1   # identifiant du prochain NFT à créer
        self.blockchain = Blockchain()  # blockchain pour enregistrer les opérations (TP)
        self.mintingOpen = False  # indique si période de minting est ouverte

        # seul ce propriétaire est autorisé par défaut à mint.
        self.authorizedMinters = set()
        self.authorizedMinters.add(ownerPublicKey)

        #image de la collection
        self.imagePath = os.path.join("..","imprimerie")
        self.availableImages = []
        for file in os.listdir(self.imagePath):
            if file.endswith(".png", ".jpg", ".webp"):
                self.availableImages.append(file)


    # méthodes : ajouter, retirer, autoriser minting, mint, transferer

    def add_minter(self, userPublicKey, otherPublicKey):
        # ajout d'un minter par se clé publique
        if otherPublicKey != self.ownerPublicKey:
            raise Exception("Pas autorisé à ajouter un minter")
        self.authorizedMinters.add(userPublicKey)

    def remove_minter(self, userPublicKey, otherPublicKey):
        # retire un minter par sa clé publique 

        if otherPublicKey != self.ownerPublicKey:
            raise Exception("Pas autorisé à retirer un minter")
        self.authorizedMinters.remove(userPublicKey)


    def open_mint(self, userPublicKey):
        # ouvre la période de minting

        # vérification de la clé de l'utilisateur
        if userPublicKey != self.ownerPublicKey:
            raise Exception("Pas autorisé à ouvrir le minting")
        self.mintingOpen = True
        self.mintStart = now()
        self.mintEnd = self.mintStart + self.mintDuration

    
    def mint(self, userPublicKey):
        current_time = now()
        # vérification de l'autorisation à mint
        # s'assurer de la période de minting
        if not self.mintingOpen or current_time > self.mintEnd:
            raise Exception("Période de minting fermée")
        
        # dépassement de la limite de la collection
        if self.nextTokenId > self.limit:
            raise Exception("plus de place dans la collection NFTs")
        
        # vérification autorisation du user
        if userPublicKey not in self.authorizedMinters:
            raise Exception("Utilisateur non autorisé à mint")
        
        # banque d'image vide (imprimerie)
        if not self.availableImages:
            raise Exception("Plus de NFTs disponible\nRajouter encre à l'imprimerie")
        
        # création du NFT

        metadata = random.choice(self.availableImages)
        self.availableImages.remove(metadata) # on retire l'image de la banque

        tokenId = self.nextTokenId
        newNFT = NFT(tokenId, metadata, userPublicKey)
        self.nftRegistry[tokenId] = newNFT

        # certificat de minting
        mintCert = Certificate(userPublicKey)
        payload = mintCert.build_payload()
        payload['action'] = 'minting'
        payload['token_id'] = tokenId
        payload['metadata'] = metadata


        # Enregistrement sur la blockchain

        latestBlock = self.blockchain.get_latest_block()
        newBlock = Block(
            userPublicKey,
            len(self.blockchain.blockList),
            latestBlock.hash(),
            [mintCert]
        )
        self.blockchain.blockList.append(newBlock)

        self.nextTokenId += 1
        
        return tokenId
    


    def transfer(self, tokenId, senderPublicKey, recieverPublicKey):

        # verification si token dans la liste de nft
        if tokenId not in self.nftRegistry:
            raise Exception("Error 404 : NFT introuvable")
        nft = self.nftRegistry[tokenId]

        if nft.ownerPublicKey != senderPublicKey:
            raise Exception("Error : Pas autorisé à transferer le NFT")
        
        # met à jour ownerPublicKey du NFT

        nft.ownerPublicKey = recieverPublicKey

        # certificat de transfert

        transferCert = Certificate(senderPublicKey)
        payload = transferCert.build_payload()
        payload['action'] = 'transfer'
        payload['token_id'] = tokenId
        payload['new_owner'] = recieverPublicKey

        # modification de la blockchain

        latestBlock = self.blockchain.get_latest_block()
        newBlock = Block(
            senderPublicKey,
            len(self.blockchain.blockList),
            latestBlock.hash(),
            [transferCert] 
        )
        self.blockchain.blockList.append(newBlock)
        
        return True
    
    

    # Affichage de la collection 

    def display(self):
        nfts_display = [nft.display() for nft in self.nftRegistry.values()]
        info_collection = {
            'owner' : self.ownerPublicKey,
            'limit' : self.limit,
            'mintingOpen' : self.mintingOpen,
            'mintStart' : self.mintStart,
            'NFTs' : nfts_display,
            'blockchain' : self.blockchain.display()
        }

        return info_collection

        



    



    

    
 
        

