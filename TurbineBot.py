import discord
from discord.ext import commands
from math import pow, sqrt, ceil, sin, pi
from math import log as ln
import asyncio
import re

token = [REDACTED]
enabled_channel = [REDACTED]


bladeStats = {"trinitite": [0.6, 0.0, True], "thorium": [0.65, 0.0, True], "du": [0.7, 0.0, True],
              "stator": [0.75, 0.0, True], "e60": [0.8, 0.0, True], "une-90": [0.85, 1.0, False],
              "une-192": [0.9, 1.1, False], "une-231": [0.95, 1.2, False], "edelstahl": [1.25, 1.5, False],
              "niosteel": [1.35, 1.0, False], "steel": [1.4, 1.0, False], "neptunium": [1.45, 1.03, False],
              "plutonium": [1.50, 1.06, False], "legierung": [1.50, 1.5, False], "extnio": [1.55, 1.1, False],
              "extreme": [1.6, 1.1, False], "americium": [1.65, 1.13, False], "curium": [1.7, 1.16, False],
              "sicnio": [1.75, 1.2, False], "matrix": [1.75, 1.5, False], "sic": [1.8, 1.2, False],
              "berkelium": [1.9, 1.23, False], "californium": [2.2, 1.27, False], "pancake": [16.0, 1.05, False]}

bladeAliases = {"trinitite": ["trinitite", "tri", 752973193878175825],
                "thorium": ["thorium", "th", "ths", 752973193710665809],
                "du": ["du", "dus", 752973193740026008],
                "stator": ["stator", "sta", "st", 752974289866719253],
                "e60": ["e60", "e-60", "elektron60", 752973194033365042],
                "une-90": ["une-90", "unwieldy-90", "une90", 752973096742289428],
                "une-192": ["une-192", "unwieldy-192", "une192", 752973096922644520],
                "une-231": ["une-231", "unwieldy-231", "une231", 752973096700608615],
                "edelstahl": ["edelstahl", "ultralight-edelstahl", "ul-edel", "ultralightedelstahl", "ule", 752973096738226316],
                "niosteel": ["niosteel", "niobium-steel", "nios", 752973097044279437],
                "steel": ["steel", "ste", "s", 752974289766187068],
                "neptunium": ["neptunium", "np", 752973096884895866],
                "plutonium": ["plutonium", "pu", 752973097170239498],
                "legierung": ["legierung", "ultralight-legierung", "ul-legie", "ultralightlegierung", "ull", 752973096641888348],
                "extnio": ["extnio", "extremenio", "extreme-nio", "enio", 752973097040347167],
                "extreme": ["extreme", "ext", "ex", 752974289719918663],
                "americium": ["americium", "am", 752973096561934437],
                "curium": ["curium", "cm", 752973096608071770],
                "sicnio": ["sicnio", "sicniosic", 752973097300131890],
                "matrix": ["matrix", "ultralight-matrix", "ul-matrix", "ultralightmatrix", "ulm", 752973096771780721],
                "sic": ["sic", "sicsiccmc", "sicsic", 752974289569054752],
                "berkelium": ["berkelium", "bk", 752973096553676931],
                "californium": ["californium", "cf", 752973096566128790],
                "pancake": ["pancake", "cake", 752973097019375617]}

bladeConversions = {"trinitite": "0", "thorium": "1", "du": "2", "stator": "3", "e60": "4", "une-90": "5",
                    "une-192": "6", "une-231": "7", "edelstahl": "8", "niosteel": "9", "steel": "a", "neptunium": "b",
                    "plutonium": "c", "legierung": "d", "extnio": "e", "extreme": "f", "americium": "g", "curium": "h",
                    "sicnio": "i", "matrix": "j", "sic": "k", "berkelium": "l", "californium": "m", "pancake": "n"}

gasStats = {"hps": [16.0, 4.0], "lps": [4.0, 2.0], "steam": [4.0, 2.0], "scs": [16.0, 16.0], "scco2": [24.0, 8.0],
              "n2": [11.0, 2.0], "co2": [14.0, 3.0], "he": [30.0, 4.0], "ar": [12.0, 2.0], "ne": [25.0, 8.0],
              "kr": [17.0, 5.0], "xe": [22.0, 6.0]}

gasAliases = {"hps": ["hps", "High Pressure Steam", "highpressuresteam", "hpsteam"],
                "lps": ["lps", "Low Pressure Steam", "lowpressuresteam", "lpsteam"],
                "steam": ["steam", "Steam", "meksteam", "tes", "forgesteam", "testeam"],
                "scs": ["scs", "Supercritical Steam", "supercriticalsteam", "scsteam"],
                "scco2": ["scco2", "Supercritical Carbon Dioxide", "supercriticalco2",
                          "supercriticalcarbondioxide", "sco2", "scarbondioxide", "sccarbondioxide"],
                "n2": ["n2", "Hot Nitrogen", "nitrogen", "hotnitrogen", "hotn2"],
                "co2": ["co2", "Hot Carbon Dioxide", "carbondioxide", "hotco2", "hotcarbondioxide"],
                "he": ["he", "Hot Helium", "helium", "hothelium", "hothe"],
                "ar": ["ar", "Hot Argon", "argon", "hotargon", "hotar"],
                "ne": ["ne", "Hot Neon", "neon", "hotneon", "hotne"],
                "kr": ["kr", "Hot Krypton", "krypton", "hotkrypton", "hotkr"],
                "xe": ["xe", "Hot Xenon", "xenon", "hotxenon", "hotxe"]}

overhaulAliases = ["overhaul", "oh", "nco", "over"]
preoverhaulAliases = ["pre-overhaul", "po", "underhaul", "preoverhaul", "uh", "nc"]

client = commands.Bot(command_prefix="&")
client.remove_command("help")


# controls embed menus
async def embedSetup(ctx, embeds: list):
    page = 0
    botMessage = await ctx.send(embed=embeds[page])
    if len(embeds) > 1:
        await botMessage.add_reaction("\U0000274C")
        await botMessage.add_reaction("\U000025C0")
        await botMessage.add_reaction("\U000025B6")

        def check(r, u):
            return u == ctx.message.author and str(r.emoji) in ("\U000025B6", "\U000025C0", "\U0000274C")

        while True:
            try:
                react, user = await client.wait_for("reaction_add", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await botMessage.clear_reactions()
                break
            else:
                if str(react.emoji) == "\U000025B6":
                    page += 1
                    if page == len(embeds):
                        page = 0
                    await botMessage.edit(embed=embeds[page])
                    await botMessage.remove_reaction(emoji="\U000025B6", member=user)
                elif str(react.emoji) == "\U000025C0":
                    page -= 1
                    if page == -1:
                        page = len(embeds) - 1
                    await botMessage.edit(embed=embeds[page])
                    await botMessage.remove_reaction(emoji="\U000025C0", member=user)
                elif str(react.emoji) == "\U0000274C":
                    await botMessage.clear_reactions()
                    break


# calculate stats
def calcStats(mode, gasName, gasRFMB, gasExp, blades, dims, gasInput, coilEff):
    def idealMult(ideal, actual):
        return min(ideal, actual)/max(ideal, actual)

    actualExp, idealExp, embedsList = [], [], []
    totalExp, bladeMult, minStatorExp, maxStatorExp, minBladeExp = 1.0, 0.0, 1.0, 2.0**(-1000), 2.0**1000
    maxBladeExp, throughputBonus = 1.0, 1.0
    statorCount, minInput = 0, 0
    rotorsDict = {alias: 0 for alias in list(bladeAliases)}
    bladeString, statsString, blocksString, rotorsString, footerText, footer2Text = "", "", "", "", "", ""
    turbineString = "/{0}/{1}/{2}/{3}".format(mode, gasName, gasRFMB, gasExp)
    if dims is not None:
        turbineString += "/{0}/{1}/".format(dims[0], dims[1])
    if gasName != "Custom":
        gasName = gasAliases[gasName][1]

    for i in range(len(blades)):
        currentBlade = bladeStats[blades[i]]
        prevExp = totalExp
        idealExp.append(pow(gasExp, (i + 0.5)/len(blades)))
        totalExp *= currentBlade[0]
        bladeString += "{} ".format(client.get_emoji(bladeAliases[blades[i]][-1]))
        rotorsDict[blades[i]] += 1
        if currentBlade[2]:
            statorCount += 1
        if mode in preoverhaulAliases:
            actualExp.append((prevExp + totalExp)/2)
            if blades[i] == "sic":
                bladeMult += 0.05*idealMult(idealExp[i], actualExp[i])
        elif mode in overhaulAliases:
            actualExp.append(prevExp*sqrt(currentBlade[0]))
            if currentBlade[2]:
                minStatorExp = min(minStatorExp, currentBlade[0])
                maxStatorExp = max(maxStatorExp, currentBlade[0])
            else:
                minBladeExp = min(minBladeExp, currentBlade[0])
                maxBladeExp = max(maxBladeExp, currentBlade[0])

        bladeMult += currentBlade[1]*idealMult(idealExp[i], actualExp[i])
        if dims is not None:
            turbineString += "{0}".format(bladeConversions[blades[i]])
    turbineString += "/"

    try:
        bladeMult /= len(blades) - statorCount
    except ZeroDivisionError:
        bladeMult = 0.0

    energyDensity = gasRFMB*bladeMult*idealMult(gasExp, totalExp)

    if dims is not None:  # dims is the tuple (turbineDim, bearingDim) or None if dims aren't input!
        shaftLen = len(blades)
        bearings = 2*dims[1]**2
        frames = 8*(dims[0] + 1) + 4*shaftLen
        casings = 2*(dims[0] ** 2) + 4*(dims[0]*shaftLen) - 2*bearings - 3  # assumes coils = bearings, 1 inlet & 1 outlet
        coils = min(bearings, 2*dims[0]**2 - bearings - 2)
        if bearings > dims[0]**2:  # if bearings are more than half the in/out surface area, all casings are covered by coils
            casings = 4*(dims[0]*shaftLen) - 1
        shafts = (bearings*shaftLen) // 2
        bladeArea = 2*dims[1]*(dims[0]-dims[1])
        maxInput = bladeArea*(shaftLen - statorCount)*100

        if gasInput is None:
            gasInput = maxInput

        if mode in overhaulAliases:
            # low throughput penalty
            if gasExp <= 1.0 or maxBladeExp <= 1.0:
                effMinLen = 24.0
            else:
                effMinLen = ceil(ln(gasExp)/ln(maxBladeExp))
            absLeniency = 400*effMinLen
            minInput = int(max(0, 0.75*maxInput - absLeniency))

            if maxInput == 0:
                throughputRatio = 1.0
            else:
                throughputRatio = min(1.0, (absLeniency + gasInput)/maxInput)

            if throughputRatio >= 0.75:
                throughputPenalty = 1.0
            else:
                throughputPenalty = 0.5*sin(throughputRatio*pi/1.5) + 0.5

            # high throughput bonus
            if minBladeExp <= 1.0 or minStatorExp >= 1.0:
                effMaxLen = 24
            else:
                effMaxLen = max(1, min(24, ceil(ln(gasExp) - 24*(ln(minStatorExp)/ln(minBladeExp/minStatorExp)))))

            lengthBonus = gasInput/(100.0 * effMaxLen * bladeArea)
            areaBonus = sqrt(gasInput/(1200.0 * shaftLen * effMaxLen))
            throughputBonus = 1 + pow(lengthBonus*areaBonus, 2.0/3.0)

            energyDensity *= throughputPenalty*throughputBonus

        if coilEff is not None:
            energyDensity *= coilEff

        powerOutput = int(energyDensity*gasInput)

        # create field strings
        # field 1.2: turbine stats (field 1.1, gas stats is created on embed creation later)
        if mode in overhaulAliases:
            gasInput = min(gasInput, 2*maxInput)
            statsString = "Dimensions: {0}x{0}x{1} ({2}x{2} Bearing)\n" \
                          "Power Output\*: {3:,} RF/t\n" \
                          "Total Expansion: {4:.2%} [{5:g} x {6:.2%}]\n" \
                          "Rotor Efficiency: {9:.2%}\n" \
                          "Throughput Bonus: {7:.2%}\n" \
                          "Energy Density\*: {8:.2f} RF/mB\n".format(dims[0], shaftLen, dims[1], powerOutput, totalExp,
                                                                     gasExp, totalExp/gasExp, throughputBonus,
                                                                     energyDensity, bladeMult)
            if gasInput:
                statsString += "Input Rate: {0:,}/{1:,} mB/t [{2:.0%}]\n".format(gasInput, maxInput, gasInput/maxInput)
                footerText = "*Dynamo efficiency not included.\n"
                if coilEff:
                    statsString += "Dynamo Efficiency: {0:.2%}\n".format(coilEff)
                    footerText = "*Dynamo efficiency included.\n"
            else:
                statsString += "Min Input\*\*: {0:,} mB/t\nMax Safe Input: {1:,} mB/t\n".format(minInput, maxInput)
                footerText = "*Dynamo efficiency not included.\n**Minimum mB/t of gas needed for no penalty.\n"
        elif mode in preoverhaulAliases:
            gasInput = min(gasInput, maxInput)
            statsString = "Dimensions: {0}x{0}x{1} ({2}x{2} Bearing)\n" \
                          "Power Output\*: {3:,} RF/t\n" \
                          "Total Expansion: {4:.2%} [{5:g} x {6:.2%}]\n" \
                          "Rotor Efficiency: {8:.2%}\n" \
                          "Energy Density\*: {7:.2f} RF/mB\n".format(dims[0], shaftLen, dims[1], powerOutput, totalExp,
                                                                     gasExp, totalExp / gasExp, energyDensity, bladeMult)
            if gasInput:
                statsString += "Input Rate: {0:,}/{1:,} mB/t [{2:.0%}]\n".format(gasInput, maxInput, gasInput/maxInput)
                if coilEff is None:
                    footerText = "*Dynamo efficiency not included.\n"
                else:
                    statsString += "Dynamo Efficiency: {0:.2%}\n".format(coilEff)
                    footerText = "*Dynamo efficiency included.\n"

        # field 2.1: blocks required string
        if mode in overhaulAliases:
            blocksString = "Casings (total): {4} ({0})*\nCasings (as frame): {1}\nBearings: {2}\nShafts: {3}\nCoils: {5}\n" \
                           "Inlets: 1\nOutlets: 1\nController: 1\n".format(casings, frames, bearings, shafts,
                                                                           casings + frames, coils)
            footer2Text = "*Turbine glass needed for transparent turbine.\n"
        elif mode in preoverhaulAliases:
            blocksString = "Casings: {0}\nFrames: {1}\nBearings: {2}\nShafts: {3}\nCoils: {4}\n" \
                           "Inlets: 1\nOutlets: 1\nController: 1\n".format(casings, frames, bearings, shafts, coils)

        # field 2.2: rotor blade string
        rotorsString += "Total Blades: {:,}\n".format(bladeArea * shaftLen)
        for rotorName, rotorCount in rotorsDict.items():
            if rotorCount == 0:
                continue
            else:
                rotorsString += "{0} x{1:,}\n".format(client.get_emoji(bladeAliases[rotorName][-1]), rotorCount*bladeArea)

    # alternative field 1.2 when dimensions are not input
    else:
        statsString = "Shaft Length: {0}\nTotal Expansion: {1:.2%} [{2:g} x {3:.2%}]\n" \
                      "Rotor Efficiency: {4:.2%}\nEnergy Density\*: {5:.2f} RF/mB".format(len(blades), totalExp,
                                                                                        gasExp, totalExp/gasExp,
                                                                                        bladeMult, energyDensity)
        footerText = "*Any coil and gas input modifiers not included.\n"

    # produce embeds
    statsPage1 = discord.Embed(title="{} Turbine (Stats)".format(mode.capitalize()), colour=0x123456, description=
                               "An overview of the given turbine's stats.")
    statsPage1.add_field(name="Blade Configuration", value=bladeString, inline=False)
    statsPage1.add_field(name="Gas Stats", value="Name: {0}\nBase Energy: {1:g} RF/mB\nIdeal Expansion: {2:.0%}\n"
                         .format(gasName, gasRFMB, gasExp), inline=False)
    statsPage1.add_field(name="Turbine Stats", value=statsString, inline=False)
    statsPage1.set_footer(text="{}Turbine Calculator Bot by FishingPole#3673".format(footerText))
    embedsList = [statsPage1]
    if dims is not None:
        statsPage1.add_field(name="Turbine String (Copy & paste in &stats command)", value=turbineString, inline=False)
        statsPage2 = discord.Embed(title="{} Turbine (Blocks)".format(mode.capitalize()), colour=0x123456, description=
                                   "An overview of the blocks required to build the turbine.")
        statsPage2.add_field(name="Blocks Required", value=blocksString, inline=False)
        statsPage2.add_field(name="Blades Required", value=rotorsString, inline=False)
        statsPage2.set_footer(text="{}Turbine Calculator Bot by FishingPole#3673".format(footer2Text))
        embedsList.append(statsPage2)

    return embedsList


@client.event
async def on_ready():
    print('Bot online as {0.user}'.format(client))


@client.command()
async def ping(ctx):
    if ctx.channel.id == enabled_channel:
        await ctx.send("Pong! `{:.0f} ms`".format(client.latency*1000))


@client.command()
async def smore(ctx):
    if ctx.channel.id == enabled_channel:
        await ctx.send("S'more! {}".format(str(client.get_emoji(493612965195677706))))


@client.command()
async def praise(ctx):
    if ctx.channel.id == enabled_channel:
        await ctx.send("{}".format(str(client.get_emoji(588415212223201327))))


@client.command(aliases=["ban", "banhammer"])
async def banned(ctx):
    if ctx.channel.id == enabled_channel:
        await ctx.send("{}".format(str(client.get_emoji(717806537967534232))))


@client.command(aliases=["fishingpole", "FishingPole", "thepolethatfishes", "ThePoleThatFishes"])
async def pole(ctx):
    if ctx.channel.id == enabled_channel:
        await ctx.send("{}".format(str(client.get_emoji(711260788215644230))))


@client.command()
async def help(ctx):
    helpPage1 = discord.Embed(title="Help menu (Page 1)", colour=0x123456, description="A list of available commands!")
    helpPage1.add_field(name="&calc/&turbine/&plan", value="Calculate a turbine given some parameters. Syntax:\n"
    "`&calc [mode] [fuel] (dimensions) [blades]` or \n"
    "`&calc [mode] [base RF/mB] [ideal expansion] (dimensions) [blades]`\n"
    "See page 2 for more details!")
    helpPage1.add_field(name="&stats", value="Calculate a turbine's stats using specific input rate and dynamo efficiency. Syntax:\n"
                                             "`&stats [turbine string] [input rate] (dynamo efficiency)`\n"
                                             "See page 3 for more details!", inline=False)
    helpPage1.add_field(name="&ping", value="The infamous ping command. Returns ping (in ms) of the bot.", inline=False)
    helpPage1.add_field(name="&help", value="Prints this message.", inline=False)
    helpPage1.add_field(name="Navigation", value="You can navigate the embeds by adding to the reactions of the bot.\n"
    "▶ goes to the next page,\n◀ goes to the previous page,\n❌ exits the navigation menu.")
    helpPage1.set_footer(text="Turbine Calculator Bot by FishingPole#3673")
    helpPage2 = discord.Embed(title="Help menu (Page 2)", colour=0x123456, description="[List of Aliases]({})".format(
        "https://github.com/ThePoleThatFishes/Turbine-Bot/blob/master/aliases.txt"
    ))
    helpPage2.add_field(name="&calc Details", value="`mode`: The calculation mode. Refers to overhaul or pre-overhaul"
    " NC.\nCheck list of aliases at the top for valid names.\n`fuel`: The type of gas that"
    " enters the turbine. Usually a type of steam.\nValid names can be found in the list of aliases.\n`base RF/mB`: "
    "The base energy density of the gas (Can be decimal).\n**__Not compatible with fuel"
    " type!__**\n`ideal expansion`: The ideal expansion of the gas. \nWritten as a number (eg. 400% = 4). **__Not compatible"
    " with fuel type!__**\n`dimensions`: Turbine & Bearing dimensions. Written as `txby`, x is turbine diameter\n"
    "and y is bearing diameter. **__Optional Parameter__**\n"
    "`blades`: The blades used in the turbine. Each blade is separated by a space.\nValid names can be found in the list"
    " of aliases.", inline=False)
    helpPage2.add_field(name="Example of a &calc command", value="`&calc nco hps steel ext s`\nA turbine in NC Overhaul, with"
    " unspecified dimensions, that uses high pressure steam, and blades used are steel extreme steel.\n `&calc nc lps t8b4 s s`\n"
    "A 8x8x2 pre-overhaul turbine that has a 4x4 bearing, uses low pressure steam and blades used are steel steel.", inline=False)
    helpPage2.set_footer(text="Turbine Calculator Bot by FishingPole#3673")
    helpPage3 = discord.Embed(title="Help menu (Page 3)", colour=0x123456)
    helpPage3.add_field(name="&stats Details", value="`turbine string`: A string that describes the turbine's dimensions, "
                                                     "blades, fuel, etc. Obtained by running &calc on your desired turbine.\n"
                                                     "`input rate`: The gas input rate in mB/t.\n"
                                                     "`dynamo efficiency`: The dynamo (coil) efficiency of the turbine.\n"
                                                     "Can be a number or a percentage (eg. 1.039 or 103.9%) "
                                                     "**__Optional Parameter__**", inline=False)
    helpPage3.add_field(name="Example of a &stats command", value="`&stats /overhaul/hps/16.0/4.0/10/4/aaaa/ 1450 101%`\n"
                                                                  "This will calculate the stats of a turbine in overhaul,\n"
                                                                  "that runs high pressure steam, is 10x10x4, has a 4x4 bearing,\n"
                                                                  "blades are all steel, input rate is 1450 mB/t,\n"
                                                                  "and dynamo efficiency is 101%.", inline=False)
    helpPage3.set_footer(text="Turbine Calculator Bot by FishingPole#3673")
    if ctx.channel.id == enabled_channel:
        await embedSetup(ctx, [helpPage1, helpPage2, helpPage3])


@client.command(aliases=["turbine", "plan"])
async def calc(ctx, *args):  # args: (overhaul/underhaul) (RF density) (ideal expansion) (blades)
    blades = []
    gasName, inputError, args = None, False, list(args)
    error, turbineDim, bearingDim, dimsInput = "", 3, 1, False
    sanitizeInput = ("*", "_", "`", "~", ",")

    for i in range(len(args)):
        for md in sanitizeInput:
            args[i] = args[i].replace(md, "")

    # checks if there's enough arguments
    try:
        # checks calculation mode (1st argument)
        if (args[0].lower()).replace(" ", "") not in overhaulAliases + preoverhaulAliases:
            inputError = True
            error += "\"{}\" is not a valid calculation mode!\n".format(args[0])
        else:
            args[0] = (args[0].lower()).replace(" ", "")
            if args[0] in overhaulAliases:
                args[0] = overhaulAliases[0]
            elif args[0] in preoverhaulAliases:
                args[0] = preoverhaulAliases[0]

        # checks if the 2nd argument is a steam type or RF density, checks for invalid steam & invalid RF/mb
        try:
            typeDetection = float(args[1])
            if typeDetection <= 0.0:
                inputError = True
                error += "Turbine fuel must have a positive energy density!\n"

            try:
                if args[2].endswith("%"):
                    args[2] = args[2].replace("%", "")
                    args[2] = float(args[2])/100.0
                else:
                    args[2] = float(args[2])
                if args[2] <= 0.0:
                    inputError = True
                    error += "Turbine fuel must have a positive expansion coefficient!\n"
            except ValueError:
                inputError = True
                error += "Missing expansion coefficient parameter!\n"

            gasName = "Custom"

            # checks if turbine dimensions have been entered
            if re.search("t[0-9]", args[3]):
                try:
                    bearingDetect = (args[3].lower()).index("b")
                    turbineDim = int(args[3][1:bearingDetect])
                    if not (3 <= turbineDim <= 24):
                        inputError = True
                        error += "Turbine diameter must be between 3 and 24 blocks!\n"
                    try:
                        bearingDim = int(args[3][bearingDetect + 1:])
                        if not (1 <= bearingDim <= turbineDim - 2 and turbineDim % 2 == bearingDim % 2):
                            inputError = True
                            error += "Bearing diameter must be between 1 and Turbine diameter - 2! If turbine " \
                                     "diameter is even, bearing must be even; The same applies for odd turbine diameter.\n"
                        else:
                            dimsInput = True
                            blades = args[4:]
                    except ValueError:
                        inputError = True
                        error += "Invalid bearing dimension!"
                except IndexError:
                    inputError = True
                    error += "Turbine dimensions \"{}\" are invalid!"

            else:
                dimsInput = False
                blades = args[3:]

        except ValueError:

            try:
                typeDetection = float(args[2])
                inputError = True
                error += "You can't have both a fuel type and an ideal expansion!\n"
            except ValueError:
                pass

            steamFound = False
            gasName = args[1]

            for aliases in gasAliases.values():
                if (gasName.lower()).replace(" ", "") in aliases:
                    gasName = aliases[0]
                    steamFound = True
                    break

            if steamFound and (args[0] in preoverhaulAliases
                               and gasName not in ("hps", "lps", "steam")):
                inputError = True
                error += "Turbine fuel \"{}\" can't be used in {}!\n".format(gasName, args[0])

            if not steamFound:
                inputError = True
                error += "Turbine fuel \"{}\" is invalid!\n".format(gasName)

            # checks for dimensions
            if re.search("t[0-9]", args[2]):
                try:
                    bearingDetect = (args[2].lower()).index("b")
                    turbineDim = int(args[2][1:bearingDetect])
                    if not (3 <= turbineDim <= 24):
                        inputError = True
                        error += "Turbine diameter must be between 3 and 24 blocks!\n"
                    try:
                        bearingDim = int(args[2][bearingDetect + 1:])
                        if not (1 <= bearingDim <= turbineDim - 2 and turbineDim % 2 == bearingDim % 2):
                            inputError = True
                            error += "Bearing diameter must be between 1 and Turbine diameter - 2! If turbine " \
                                     "diameter is even, bearing must be even; The same applies for odd turbine diameter.\n"
                        else:
                            dimsInput = True
                            blades = args[3:]
                    except ValueError:
                        inputError = True
                        error += "Invalid bearing dimension!"
                except IndexError:
                    inputError = True
                    error += "Turbine dimensions \"{}\" are invalid!"

            else:
                dimsInput = False
                blades = args[2:]

        # checks for invalid blades
        for i1 in range(len(blades)):
            bladeFound = False

            for aliases in bladeAliases.values():
                if blades[i1].startswith("<"):
                    colon2 = blades[i1].find(":", 2)
                    blades[i1] = blades[i1][2:colon2]
                else:
                    blades[i1] = (blades[i1].lower()).replace(" ", "")

                if blades[i1] in aliases:
                    bladeFound = True
                    blades[i1] = aliases[0]

            if bladeFound and (args[0] in preoverhaulAliases
                               and blades[i1] not in ("stator", "steel", "extreme", "sic")):
                inputError = True
                error += "Blade #{} ({}) does not exist in {}!\n".format(i1 + 1, blades[i1], args[0])

            if not bladeFound:
                inputError = True
                error += "Blade #{} ({}) is invalid!\n".format(i1 + 1, blades[i1])
    except IndexError:
        inputError = True
        error += "At least one argument is missing!\n"

    if len(blades) > 24:
        inputError = True
        error += "This turbine is too long!\n"

    if not inputError:
        mode = args[0]
        if gasName not in list(gasStats):
            gasRFMB = float(args[1])
            gasExp = float(args[2])
        else:
            gasRFMB = gasStats[gasName][0]
            gasExp = gasStats[gasName][1]

        if dimsInput:
            embedsList = calcStats(mode, gasName, gasRFMB, gasExp, blades, (turbineDim, bearingDim), None, None)
        else:
            embedsList = calcStats(mode, gasName, gasRFMB, gasExp, blades, None, None, None)

        if ctx.channel.id == enabled_channel:
            await embedSetup(ctx, embedsList)

    else:
        results = discord.Embed(title="Error in command!", colour=0xd50505, description="Oh no! The bot could not"
                                                                                      " calculate the turbine!")
        if len(error) > 1000:
            error = "{}... (too long)".format(error[:1000])
        results.add_field(name="Errors detected:", value="{}".format(error), inline=False)
        results.set_footer(text="Turbine Calculator Bot by FishingPole#3673")
        if ctx.channel.id == enabled_channel:
            await embedSetup(ctx, [results])


@client.command()
async def stats(ctx, *args):  # &stats (turbine string) (mB/t input) (coil efficiency)
    args, inputError = list(args), False
    turbineInfo, bladeList, embedsList, errorString = [], [], [], ""

    try:
        args[1] = int(args[1])
        if args[1] < 0:
            inputError = True
            errorString += "Gas input must be a positive number!\n"
    except ValueError:
        inputError = True
        errorString += "Gas input must be a positive number!\n"

    try:
        if args[2].endswith("%"):
            args[2] = args[2].replace("%", "")
            args[2] = float(args[2])/100.0
        else:
            args[2] = float(args[2])
    except IndexError:
        args.append(None)
    except ValueError:
        inputError = True
        errorString += "Dynamo efficiency must be a positive number!\n"

    if not inputError:
        if args[0].count("/") == 8:
            slash2 = 0
            for i in range(7):
                slash1 = slash2
                slash2 = args[0].find("/", slash1 + 1)
                turbineInfo.append(args[0][slash1 + 1:slash2])

        for char in turbineInfo[-1]:
            if char in bladeConversions.values():
                charPos = list(bladeConversions.values()).index(char)
                bladeList.append(list(bladeConversions)[charPos])

        embedsList = calcStats(turbineInfo[0], turbineInfo[1], float(turbineInfo[2]), float(turbineInfo[3]), bladeList,
                               (int(turbineInfo[4]), int(turbineInfo[5])), args[1], args[2])
    else:
        errorEmbed = discord.Embed(title="Error in command!", colour=0xd50505, description="Oh no! The bot could not"
                                                                                        " calculate the turbine!")
        errorEmbed.add_field(name="Errors detected:", value="{}".format(errorString), inline=False)
        errorEmbed.set_footer(text="Turbine Calculator Bot by FishingPole#3673")
        if ctx.channel.id == enabled_channel:
            await embedSetup(ctx, [errorEmbed])

    await embedSetup(ctx, embedsList)


client.run(token)
