
import discord 
from discord.ext import commands 
import datetime
import json
import requests
import time
import asyncio
import flask
from flask import keep_alive
import os 


client = commands.Bot(command_prefix='!' , intents=discord.Intents.all())
client.remove_command("help")

#custom-help--

@client.group(invoke_without_command = True )
async def help(ctx):
	embed = discord.Embed(title = "help" , description = "Use [ !help ] for extended information.. " , color = ctx.author.color)
	embed.add_field(name= "adrole" , value = "!adrole (-mantion-role-) (mention-time/in seconde format [example - 12h = 43200 seconde]) (mention-users) Given role will be automatically removed after time gets over !")
	embed.add_field(name = "reactrole" , value = "reactrole (emoji-rolename-about role) ")
	embed.add_field(name = "Person information" , value = "profile (mention.user) , wi (mention.user)")
	embed.add_field(name = "invite" , value = " invite ")
	embed.add_field(name = "clear" ,value ="clear command")
	embed.add_field(name = "version" , value = "Maneger bot vr - 1.1.0 ")

	
	await ctx.send(embed=embed)






@client.event
async def on_ready():
	await client.change_presence(activity=discord.Game(name=f"!! on\n {len(client.guilds)} servers | !help"))
	print("Ready")

#error-handling-

#reactions- 

@client.event
async def on_raw_reaction_add(payload):
	if payload.member.bot:
		pass
	else:
		with open('react.json') as react_file:
			data = json.load(react_file)
			for x in data:
				if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
					role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])
					await payload.member.add_roles(role)
				else :
					await payload.channel_id.send("missing Permissions")
				
					



#remove-reaction-


@client.event
async def on_raw_reaction_remove(payload):

		with open('react.json') as react_file:
			data = json.load(react_file)
			for x in data:
				if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
					role = discord.utils.get(client.get_guild(payload.guild_id).roles, id=x['role_id'])
					await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
		await member.send(embed=embed)


#react-role-command

@client.command()
@commands.has_permissions(manage_roles=True)
async def  reactrole(ctx , emoji, role: discord.Role ,*, message ):
	embed = discord.Embed(description=message ,  color = ctx.author.color)
	msg = await ctx.channel.send(embed=embed)
	await msg.add_reaction(emoji)

	with open('react.json') as json_file:
		data = json.load(json_file)

		new_react_role = {
			'role_name':role.name,
			'role_id':role.id,
			'emoji':emoji,
			'message_id':msg.id

		}

		data.append(new_react_role)
	with open('react.json' , 'w')as j:
		json.dump(data,j,indent=4)



#commands-seaction --

#clear command-

@client.command()
@commands.has_permissions(manage_messages= True)
async def clear(ctx , amount = 2):
	await ctx.channel.purge(limit= amount)


#invite

@client.command(name='invite',pass_context=True)
async def invite(ctx, *argument):
    #creating invite link
    invitelink = await ctx.channel.create_invite(max_uses=100,unique=True)
    #dming it to the person
    await ctx.author.send(invitelink)
    
 #wi
 
@client.command()
async def wi(ctx, *, user: discord.Member = None , inline = False ):
    
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.set_footer(text='ID: ' + str(user.id))
    embed.timestamp = datetime.datetime.utcnow()
  
    return await ctx.send(embed=embed)

#profile

@client.command()
async def profile(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

#modreation-commands--



#auto-role-

@client.command()
@commands.has_permissions(manage_roles=True)
async def adrole(ctx ,role : discord.Role, time : int, members : commands.Greedy[discord.Member]):
	for m in members:
		await m.add_roles(role)
	await ctx.send(f"Successfully given {role.mention} to {len(members)} Users!!")
	await asyncio.sleep(time)
	for m in members:
		await m.remove_roles(role)
	await ctx.send("Roles removed Successfully")




keep_alive()
my_secret = os.environ['TOKEN']
client.run(my_secret)

