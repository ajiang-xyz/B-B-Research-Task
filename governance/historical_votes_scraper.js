const { request } = require('graphql-request')

const endpoint = 'https://gateway.thegraph.com/api/subgraphs/id/GHB6EWsmMXy2AJaCodmK2AmZviitTZf3Tbo8YEfuh6St'
const query = `{
  votes(where: {
    voter_contains: "ADDRESS_STRING"
  }) {
    id
    voter {
      id
    }
    proposal {
      id
    }
  }
}`

// The very suspicious, contiguous blob of ~25k vote addresses that voted FOR Prop 289
// https://www.tally.xyz/gov/compound/proposal/289/votes?govId=eip155:1:0xc0Da02939E1441F497fd74F78cE7Decb17B66529
const suspicious_addresses = [
  "0x337f3fb97657b542ec3f182a488b7f7feba8bc0e",
  "0x48804e458d7a779c5fd2ce757876dabdc9ce422c",
  "0xc153a898808654584a2276bfe9e8ba62aded4137",
  "0xd9e8d24799fc9317513c0c0512f19cb60db6b040",
  "0xe89f1a18a17f0497ac2bd8627d48339d4d99bb56",
  "0x13691cff1092d704ec20e16036491c8805f6d22c",
  "0xb3180769211598e172789e185067630da2b7ce1b",
  "0x72c9812400528e04054eccd839e14c126fc13883",
  "0x90bd4645882e865a1d94ab643017bd5ec2ae73be",
  "0x3318552dec1881bfd43adfac65adee81cc6298bb",
  "0x55c03907c62cf2884b795f216e7cd1dcb5e560bf",
  "0xca4edba2cf8d23bc2ce8d62dde8832a3fcee7f02",
  "0x0b588bd4b60fb38daa5dc089ad3486b34f7700f8",
  "0x17d6dd6b29c639efca9d3ec2fe3848909c1b40d9"
]

const headers = {
  Authorization: `Bearer ${process.env.THEGRAPH_API_KEY}`,
}

async function fetchData(address) {
  try {
    const data = await request(endpoint, query.replace("ADDRESS_STRING", address), {}, headers)

    // Suspicious if:
    //     - the address only has a handful of votes total 
    //     - Prop 289 was the address' first vote
    if (data.votes.length < 5 || data.votes[0].proposal.id == "289") {
      console.log(`Suspicious address found: ${address} (${data.votes.length} total votes, first vote ${data.votes[0].proposal.id == "289" ? "WAS " : "not "}on Prop 289)`)
      for (vote of data.votes) {
        console.log(vote)
      }
      console.log()
      return true
    }
  } catch (error) {
    console.error(`Error fetching data for address ${address}: ${error.message}`)
    return false
  }
}

async function main() {
  let suspicious_count = 0
  for (let address of suspicious_addresses) {
    if (await fetchData(address)) suspicious_count++
  }

  console.log(`Checked ${suspicious_addresses.length} addresses, found ${suspicious_count} suspicious addresses.`)
}

main()

