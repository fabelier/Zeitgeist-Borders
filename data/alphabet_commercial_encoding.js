/* Based on query made the 29-01-2013 

"us" mean the suggestion is a brand or a trademark us
"uk" mean the suggestion is a brand or a trademark us
null : it's not the case
tree result is the tree most sent result over the planet by order of presentation

*/
var alphabet = [
{letter:'a',r:["us","us","uk"]},
{letter:'b',r:["uk","uk","uk"]},
{letter:'c',r:["us",null,"us"]},/* null= currency converter */
{letter:'d',r:[null,"us","uk"]},/* null= dictionary */
{letter:'e',r:["us","us","us"]},/* email = 4 */
{letter:'f',r:["us","us","us"]}, /* facebook, fb */
{letter:'g',r:["us","us","us"]}, /* all google products until  5 */
{letter:'h',r:["us",null,"us"]}, /* null = happy wheels*/
{letter:'i',r:["us","us",null]},/* null=imdb */
{letter:'j',r:[null,null,"us"]},/* null=justin bieber,java */
{letter:'k',r:[null,"us","us"]},/* null=keepvid */
{letter:'l',r:["us",null,"us"]},/* null=livescore */
{letter:'m',r:["us",null,null]},/* null=map,minecraf */
{letter:'n',r:[null,"us",null]},/* null=news,nokia*/
{letter:'o',r:[null,null,null]},/* null=omegle,old navy,opera*/
{letter:'p',r:["us","us",null]},/* null=pandora */
{letter:'q',r:[null,null,"us"]},/* null=quotes,qantas*/
{letter:'r',r:[null,null,null]},/* null=rihanna,real madrid,riveisland*/
{letter:'s',r:["us",null,null]},/* null=speedtest,samsung*/
{letter:'t',r:["us",null,null]},/* null=translate,target*/
{letter:'u',r:["us",null,null]},/* null=usps,urban dictionary */
{letter:'v',r:[null,"uk",null]},/* null=vlc,viber*/
{letter:'w',r:[null,"us",null]},/* null=wikipedia,waptrick */
{letter:'x',r:["us",null,null]},/* null=xe, factor*/
{letter:'y',r:["us","us","us"]},
{letter:'z',r:[null,"us","us"]}/* null=zara*/
]

var total =  alphabet.length*3
var num = 0 

for (var i = alphabet.length - 1; i >= 0; i--) {
	var e = alphabet[i]
	console.log(e.r)
	for (var j = e.r.length - 1; j >= 0; j--) {
		if(e.r[j]=="us" || e.r[j]=="uk"){
			num+=1
		}
	};
};

console.log(num,total)
console.log(Math.round(num/total*100),"% de compagnie US or UK dans l'ensemble du top 3 des recommandation international")
