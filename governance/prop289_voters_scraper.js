// Scrape wallet addresses, their vote counts, and their vote casts
if (typeof document === "undefined") {
    console.log("This is not a Node script. Follow the steps below:")
    console.log("1) Navigate to https://www.tally.xyz/gov/compound/proposal/289/votes?govId=eip155:1:0xc0Da02939E1441F497fd74F78cE7Decb17B66529")
    console.log(`2) Scroll to the bottom and click "Load more" until all voters are displayed.`)
    console.log("2) Copy-paste this script into the DevTools console.")
    process.exit()
}
document.querySelectorAll(".css-1qzf1ag").forEach(obj => {
    [_, votes, _, cast] = obj.querySelectorAll(".chakra-text");
    voter = obj.querySelector(".chakra-link")
    if (!voter || !votes || !cast) return;
    console.log(`${voter.href.replace("https://www.tally.xyz/gov/compound/delegate/", "")}, ${votes.innerHTML}, ${cast.innerHTML}`);
})
