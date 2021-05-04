pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "./PokemonBaseStatData.sol";

contract Pokemon is ERC721, VRFConsumerBase, Ownable, PokemonBaseStatData {
    using SafeMathChainlink for uint256;
    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => uint256) public requestIdToTokenId;

    event requestedPokemon(bytes32 indexed requestId); 
    event PokemonCreated(uint256 indexed tokenId); 
    bytes32 internal keyHash;
    uint256 internal link_fee;
    uint256 public tokenCounter;

    mapping(uint256 => PokemonBaseStats) public tokenIdToBattleStats;
    mapping(uint256 => PokemonBaseStats) public tokenIdToEvs;
    mapping(uint256 => PokemonBaseStats) public tokenIdToIvs;
    UniquePokemon[] public uniquePokemon;
    string[] public natures;
    mapping(string => string) public pokemonNameToImageURI;
    // mapping(uint256 => moves) public tokenIdToMoves;
    mapping(uint256 => uint256) public tokenIdToRNGNumber;

    // struct moves {
    //     string move1;
    //     string move2;
    //     string move3;
    //     string move4;
    // }

    struct UniquePokemon {
        string nickname;
        // eh, solidity gonna get better at this
        string item;
        bool shiny;
        string ability;
        string nature;
        uint256 level; 
    }
    
    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash, uint256 _link_fee)
    public 
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("Pokémon", "PKMON")
    {
        tokenCounter = 0;
        keyHash = _keyhash;
        link_fee = _link_fee;
        natures = ["Hardy", "Lonely", "Brave", "Adamant", "Naughty", "Bold", "Docile", "Relaxed", "Impish", "Lax", "Timid", "Hasty", "Serious", "Jolly", "Naive", "Modest", "Mild", "Quiet", "Bashful", "Rash", "Calm", "Gentle", "Sassy", "Careful", "Quirky"];
    }

    function createRandomPokemon(uint256 userProvidedSeed) 
        public returns (bytes32){
            bytes32 requestId = requestRandomness(keyHash, link_fee, userProvidedSeed);
            requestIdToSender[requestId] = msg.sender;
            emit requestedPokemon(requestId);
    }

    // function createSpecificPokemon(uint256 userProvidedSeed, string memory pokemonName) onlyOwner
    //     public returns (bytes32){
    //         bytes32 requestId = requestRandomness(keyHash, link_fee, userProvidedSeed);
    //         requestIdToSender[requestId] = msg.sender;
    //         emit requestedPokemon(requestId);
    // }

    function setIvs(uint256[] memory RNGNumbers, string memory pokemonName, uint256 tokenId) internal {
        (string memory type1, string memory type2) = getTypeFromName(pokemonName);
        PokemonBaseStats memory baseStats = pokemonNameToPokemonBaseStats[pokemonName];
        uint256 hpIv = (RNGNumbers[1] % 31) + 1;
        uint256 atkIv = (RNGNumbers[2] % 31) + 1;
        uint256 defIv = (RNGNumbers[3] % 31) + 1;
        uint256 spaIv = (RNGNumbers[4] % 31) + 1;
        uint256 spdIv = (RNGNumbers[5] % 31) + 1;
        uint256 speIv = (RNGNumbers[6] % 31) + 1;
        PokemonBaseStats memory ivs = PokemonBaseStats({hp: hpIv, def: defIv, atk: atkIv, spa: spaIv, spd: spdIv, spe: speIv, type1: type1, type2: type2, number: baseStats.number, pokemonName: pokemonName});
        PokemonBaseStats memory evs = PokemonBaseStats({hp: 0, def: 0, atk: 0, spa: 0, spd: 0, spe: 0, type1: type1, type2: type2, number: baseStats.number, pokemonName: pokemonName});

        tokenIdToIvs[tokenId] = ivs;
        tokenIdToEvs[tokenId] = evs;
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        address owner = requestIdToSender[requestId];
        // string memory tokenURI = pokemonToTokenURI[requestId];
        uint256 tokenId = tokenCounter;
        requestIdToTokenId[requestId] = tokenId;
        _safeMint(owner, tokenId);
        tokenIdToRNGNumber[tokenId] = randomNumber;
        tokenCounter = tokenCounter + 1;
    }

    function updateCreatedPokemon(uint256 tokenId, string memory pokemonName) public onlyOwner {
        uint256[] memory RNGNumbers = getManyRandomNumbers(tokenIdToRNGNumber[tokenId], 11);
        // uint256 pokemonNameIndex = (RNGNumbers[7] % listOfPokemonNames.length);
        // string memory pokemonName = listOfPokemonNames[pokemonNameIndex];
        (string memory type1, string memory type2) = getTypeFromName(pokemonName);
        string memory nature = natures[(RNGNumbers[8] % natures.length)];
        bool shiny = false;
        uint256 shinyRNG = (RNGNumbers[9] % 4096);
        if (shinyRNG == 0){
            shiny = true;
        } else {
            shiny = false;
        }
        uint256 level = (RNGNumbers[10] % 100) + 1;
        uniquePokemon.push(
            UniquePokemon(
                {
                    nickname: pokemonName,
                    item: "None",
                    shiny: shiny,
                    ability: "None",
                    nature: nature,
                    level: level
                }
            )
        );
        setIvs(RNGNumbers, pokemonName, tokenId);
        setBattleStats(pokemonName, tokenId);
        emit PokemonCreated(tokenCounter);
    }

    function getTypeFromName(string memory pokemonName) public view returns (string memory, string memory){
        PokemonBaseStats memory baseStats = pokemonNameToPokemonBaseStats[pokemonName];
        return (baseStats.type1, baseStats.type2);
    }

    function setBattleStats(string memory pokemonName, uint256 tokenId) public onlyOwner{
        // HP = floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + Level + 10
        // we bump everything up by 100, then divide by 100 at the end
        // Other Stats = floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + 5) x Nature
        PokemonBaseStats storage battleStats = tokenIdToBattleStats[tokenId];
        PokemonBaseStats storage baseStats = pokemonNameToPokemonBaseStats[pokemonName];
        PokemonBaseStats storage ivs = tokenIdToIvs[tokenId];
        PokemonBaseStats storage evs = tokenIdToEvs[tokenId];
        UniquePokemon storage pokemon = uniquePokemon[tokenId];

        battleStats.hp = getCalculatedHPStat( baseStats.hp, ivs.hp, evs.hp, pokemon.level);
        battleStats.atk = getCalculatedStat( baseStats.atk, ivs.atk, evs.atk, pokemon.level); // We don't add the nature modifier!!!
        battleStats.def = getCalculatedStat( baseStats.def, ivs.def, evs.def, pokemon.level); // We don't add the nature modifier!!!
        battleStats.spa = getCalculatedStat( baseStats.spa, ivs.spa, evs.spa, pokemon.level); // We don't add the nature modifier!!!
        battleStats.spd = getCalculatedStat( baseStats.spd, ivs.spd, evs.spd, pokemon.level); // We don't add the nature modifier!!!
        battleStats.spe = getCalculatedStat( baseStats.spe, ivs.spe, evs.spe, pokemon.level); // We don't add the nature modifier!!!
        
        battleStats.type1 = ivs.type1;
        battleStats.type2 = ivs.type2;
        battleStats.pokemonName = ivs.pokemonName;
        battleStats.number = ivs.number;
    }

    function getCalculatedStat(uint256 baseStat, uint256 baseStatIv, uint256 baseStatEvs, uint256 level) public view returns (uint256){
        // Other Stats = floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + 5) x Nature
        // We haven't add the nature modifier!!!
        return ((((2 * baseStat) + baseStatIv + (baseStatEvs / 4)) * level )/ 100) + 5;
    }

    function getCalculatedHPStat(uint256 baseStat, uint256 baseStatIv, uint256 baseStatEvs, uint256 level) public view returns (uint256){
        // HP = floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + Level + 10
        return ((((2 * baseStat) + baseStatIv + (baseStatEvs / 4)) * level )/ 100) + 10 + level;
    }

    // Could turn this into a chainlink API Call if we wanted 
    function setTokenURI(uint256 tokenId, string memory _tokenURI) public onlyOwner {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }


    function getManyRandomNumbers(uint256 randomValue, uint256 n) public pure returns (uint256[] memory expandedValues) {
        expandedValues = new uint256[](n);
        for (uint256 i = 0; i < n; i++) {
            expandedValues[i] = uint256(keccak256(abi.encode(randomValue, i)));
        }
        return expandedValues;
    }   

    

    // function setMoves(string memory move1, string memory move2,string memory move3,string memory move4, uint256 tokenId) public onlyOwner {
    //     uniquePokemon[tokenId].move1 = move1;
    //     uniquePokemon[tokenId].move2 = move1;
    //     uniquePokemon[tokenId].move3 = move1;
    //     uniquePokemon[tokenId].move4 = move1;
    // }
}


