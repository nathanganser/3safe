console.log("ok");
/* Moralis init code */
const serverUrl = "https://fzvsxlwjyz7v.usemoralis.com:2053/server";
const appId = "6BR88hZ69FhFAP61xR9trWnl2lWqN1TxCtnxw9Xa";
Moralis.start({serverUrl, appId});
console.log("initiated...")

/* Authentication code */
async function login() {
    console.log("logging in");
    let user = Moralis.User.current();
    if (!user) {
        user = await Moralis.authenticate({signingMessage: "Verify email and Generate NFT"})
            .then(async function (user) {
                console.log("logged in user:", user);
                var email = window.document.getElementById('email').value
                var cryptoAddress = user.get("ethAddress");
                console.log("crypto address:", cryptoAddress);
                console.log("email:", email);
                user.set("email", email);

                window.$.post("https://threesafe.herokuapp.com/go",
                    {
                        email: email,
                        address: cryptoAddress
                    },
                    function (data, status) {
                        console.log("Data: " + data + "\nStatus: " + status);
                    });




            }).catch(function (error) {
                console.log(error);
            });
    } else {
        console.log("already logged in.")
        loadNFTs(user);
    }
}

async function loadNFTs(user) {
    console.log("getting nft..");
    const options = {chain: 'polygon', address: user.get("ethAddress")};
    const NFTs = await Moralis.Web3API.account.getNFTs(options);
    console.log(NFTs['result']);

    NFTs['result'].forEach(function(el) {
        var li = document.createElement("li");
        var text = document.createTextNode(JSON.parse(el.metadata).name);
        li.appendChild(text);
        console.log(text);
        document.getElementById("nft").appendChild(li);
    });
    document.getElementById("nft").innerText = "Your verified emails: (loaded!)";
}


async function logOut() {
    await Moralis.User.logOut();
    console.log("logged out");
}

window.onload = function () {

    document.getElementById("btn-login").onclick = login;
    document.getElementById("btn-logout").onclick = logOut;


}
