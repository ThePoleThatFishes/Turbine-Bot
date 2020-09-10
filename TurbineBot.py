import discord
from discord.ext import commands
from math import pow, sqrt

bladeStats = {"trinitite": [0.6, 0.0, True], "thorium": [0.65, 0.0, True], "du": [0.7, 0.0, True],
              "stator": [0.75, 0.0, True], "e60": [0.8, 0.0, True], "une-90": [0.85, 1.0, False],
              "une-192": [0.9, 1.1, False], "une-231": [0.95, 1.2, False], "edelstahl": [1.25, 1.5, False],
              "niosteel": [1.35, 1.0, False], "steel": [1.4, 1.0, False], "neptunium": [1.45, 1.03, False],
              "plutonium": [1.50, 1.06, False], "legierung": [1.50, 1.5, False], "extnio": [1.55, 1.1, False],
              "extreme": [1.6, 1.1, False], "americium": [1.65, 1.13, False], "curium": [1.7, 1.16, False],
              "sicnio": [1.75, 1.2, False], "matrix": [1.75, 1.5, False], "sic": [1.8, 1.2, False],
              "berkelium": [1.9, 1.23, False], "steelcake": [2.0, 1.05, False], "californium": [2.2, 1.27, False],
              "hccake": [3.0, 1.05, False], "extcake": [4.0, 1.05, False], "tccake": [5.0, 1.05, False],
              "siccake": [16.0, 1.05, False]}

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
                "steelcake": ["steelcake", "scake", 752973097052668135],
                "californium": ["californium", "cf", 752973096566128790],
                "hccake": ["hccake", "hardcarbon-cake", 752973097174302801],
                "extcake": ["extcake", "extreme-cake", 752973096889090079],
                "tccake": ["tccake", "thermoconducting-cake", 752973096985690293],
                "siccake": ["siccake", "sicsiccmcake", 752973097019375617]}

bladeConversion = {"trinitite": "0", "thorium": "1", "du": "2", "stator": "3", "e60": "4", "une-90": "5", "une-192": "6"
                   , "une-231": "7", "edelstahl": "8", "niosteel": "9", "steel": "a", "neptunium": "b", "plutonium": "c"
                   , "legierung": "d", "extnio": "e", "extreme": "f", "americium": "g", "curium": "h", "sicnio": "i",
                   "matrix": "j", "sic": "k", "berkelium": "l", "steelcake": "m", "californium": "n", "hccake": "o",
                   "extcake": "p", "tccake": "q", "siccake": "r"}

steamStats = {"hps": [16.0, 4.0], "lps": [4.0, 2.0], "steam": [4.0, 2.0], "scs": [16.0, 16.0], "scco2": [24.0, 8.0],
              "n2": [11.0, 2.0], "co2": [14.0, 3.0], "he": [22.0, 6.0], "ar": [17.0, 5.0], "ne": [25.0, 8.0]}

steamAliases = {"hps": ["hps", "High Pressure Steam", "highpressuresteam", "hpsteam"],
                "lps": ["lps", "Low Pressure Steam", "lowpressuresteam", "lpsteam"],
                "steam": ["steam", "Steam", "meksteam", "tes", "forgesteam", "testeam"],
                "scs": ["scs", "Supercritical Steam", "supercriticalsteam", "scsteam"],
                "scco2": ["scco2", "Supercritical Carbon Dioxide", "supercriticalco2",
                          "supercriticalcarbondioxide", "sco2", "scarbondioxide", "sccarbondioxide"],
                "n2": ["n2", "Hot Nitrogen", "nitrogen", "hotnitrogen", "hotn2"],
                "co2": ["co2", "Hot Carbon Dioxide", "carbondioxide", "hotco2", "hotcarbondioxide"],
                "he": ["he", "Hot Helium", "helium", "hothelium", "hothe"],
                "ar": ["ar", "Hot Argon", "argon", "hotargon", "hotar"],
                "ne": ["ne", "Hot Neon", "neon", "hotneon", "hotne"]}

client = commands.Bot(command_prefix="&")
client.remove_command("help")

@client.event
async def on_ready():
    print('Bot online as {0.user}'.format(client))


@client.command()
async def ping(ctx):
    if ctx.channel.id in (752540645117132840, 708428479787434400):
        await ctx.send("Pong! `{:.0f} ms`".format(client.latency*1000))


@client.command()
async def help(ctx):
    helpEmbed = discord.Embed(title="Help menu", colour=0x123456, description="A list of available commands!")
    helpEmbed.add_field(name="&calc/&turbine/&plan", value="Calculates a turbine based on the following syntax:\n"
    "`&calc [mode] [fuel type] [blades]` or \n"
    "`&calc [mode] [RF/mB of fuel] [ideal expansion] [blades]`\n"
    "`mode`: Calculation mode. Can be overhaul or underhaul or preoverhaul (underhaul and preoverhaul are the same)\n"
    "`fuel type`: The type of gas that enters the turbine. See list of aliases for valid names. \n"
    "`RF/mB of fuel`: Base energy density of gas (**__not compatible with fuel type__**)\n "
    "`ideal expansion`: The ideal expansion of the gas. Must be input as a number (eg. 400% = 4) (**__not compatible with fuel type__**) \n"
    "`blades`: The blades used in the turbine. See list of aliases for valid names.\n"
    "Order of arguments matters, capitalization doesn't matter, multi-word inputs are allowed but use quotes `\"high pressure steam\"`\n"
    "[List of Aliases]({})".format("https://github.com/ThePoleThatFishes/Turbine-Bot/blob/master/aliases.txt"), inline=False)
    helpEmbed.add_field(name="&cost/&resources", value="Prints a list of blocks and blades that make a turbine. Syntax:\n"
    "`&cost [turbine diameter] [bearing diameter] [turbine string]`\n"
    "`turbine diameter`: The diameter of the turbine.\n`bearing diameter`: The diameter of the bearing.\n"
    "`turbine string`: A string that describes the blades of a turbine. Obtained from doing &calc on a turbine.\n"
    "Order of arguments matters, don't modify the string given or you may get unexpected results!", inline=False)
    helpEmbed.add_field(name="&ping", value="The infamous ping command. Returns ping (in ms) of the bot.", inline=False)
    helpEmbed.add_field(name="&help", value="Prints this message.", inline=False)
    helpEmbed.set_footer(text="Turbine Calculator Bot by FishingPole#3673")
    if ctx.channel.id in (752540645117132840, 708428479787434400):
        await ctx.send(embed=helpEmbed)


@client.command(aliases=["turbine", "plan"])
async def calc(ctx, *args):  # args: (overhaul/underhaul) (RF density) (ideal expansion) (blades)
    actualExp, idealExp, blades, emojiBlades = [], [], [], ""
    totalExp, bladeMult, statorCount, steamType, inputError, args = 1, 0, 0, None, False, list(args)
    error, turbineString = "", ""

    def idealMult(ideal, actual):
        return min(ideal, actual)/max(ideal, actual)

    # checks if there's enough arguments
    try:
        # checks calculation mode (1st argument)
        if (args[0].lower()).replace(" ", "") not in ("overhaul", "underhaul", "preoverhaul", "pre-overhaul"):
            inputError = True
            error += "\"{}\" is not a valid calculation mode!\n".format(args[0])
        else:
            args[0] = (args[0].lower()).replace(" ", "")
            turbineString += args[0][0]

        # checks if the 2nd argument is a steam type or RF density, checks for invalid steam & invalid RF/mb
        try:
            typeDetection = float(args[1])
            if typeDetection <= 0.0:
                inputError = True
                error += "Turbine fuel must have a positive energy density!\n"

            try:
                typeDetection = float(args[2])
                if typeDetection <= 0.0:
                    inputError = True
                    error += "Turbine fuel must have a positive expansion coefficient!\n"
            except ValueError:
                inputError = True
                error += "Missing expansion coefficient parameter!\n"

            blades = args[3:]
            steamType = "Custom"
        except ValueError:

            try:
                typeDetection = float(args[2])
                inputError = True
                error += "You can't have both a fuel type and an ideal expansion!\n"
            except ValueError:
                pass

            steamFound = False
            steamType = args[1]

            for aliases in steamAliases.values():
                if (steamType.lower()).replace(" ", "") in aliases:
                    steamType = aliases[0]
                    steamFound = True
                    break

            if steamFound and (args[0] in ("underhaul", "pre-overhaul", "preoverhaul")
                               and steamType not in ("hps", "lps", "steam")):
                inputError = True
                error += "Turbine fuel \"{}\" can't be used in {}!\n".format(steamType, args[0])

            if not steamFound:
                inputError = True
                error += "Turbine fuel \"{}\" is invalid!\n".format(steamType)

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
                    emojiBlades += "{} ".format(str(client.get_emoji(aliases[-1])))
                    turbineString += bladeConversion[blades[i1]]
                    break

            if bladeFound and (args[0] in ("preoverhaul", "pre-overhaul", "underhaul")
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
        turbineLength, mode = len(blades), args[0]

        if steamType not in list(steamStats):
            steamRFMB = float(args[1])
            idealExpansion = float(args[2])
        else:
            steamRFMB = steamStats[steamType][0]
            idealExpansion = steamStats[steamType][1]

        for i in range(turbineLength):
            prevExp = totalExp
            idealExp.append(pow(idealExpansion, (i + 0.5)/turbineLength))
            totalExp *= bladeStats[blades[i]][0]

            if mode == "overhaul":
                actualExp.append(prevExp*sqrt(bladeStats[blades[i]][0]))
            elif mode == "underhaul" or mode == "preoverhaul" or mode == "pre-overhaul":
                actualExp.append((prevExp + totalExp)/2)
                if blades[i] == "sic":
                    bladeMult += 0.05*idealMult(idealExp[i], actualExp[i])
            bladeMult += bladeStats[blades[i]][1]*idealMult(idealExp[i], actualExp[i])
            if bladeStats[blades[i]][2]:
                statorCount += 1

        bladeMult /= turbineLength - statorCount
        energyDensity = bladeMult * steamRFMB * idealMult(idealExpansion, totalExp)
        if steamType != "Custom":
            steamType = steamAliases[steamType][1]

        results = discord.Embed(title="{} Turbine".format(mode.capitalize()), colour=0x123456,
                              description="Stats of the given turbine:")
        results.add_field(name="Blade configuration:", value="{0}".format(emojiBlades), inline=False)
        results.add_field(name="Turbine String: (*use this to calculate resource cost*)", value="{}".format(turbineString))
        results.add_field(name="Fuel Stats:", value="Name: {}\nBase Energy: {:.0f} RF/mB\nIdeal Expansion: {:.0%}".format(
            steamType, steamRFMB, idealExpansion), inline=False)
        results.add_field(name="Turbine Stats:", value="Turbine Length: {0} \nTotal Expansion: {1:.2%} [{2:.2f} x {3:.2%}]\n"
        "Rotor Efficiency: {4:.2%}\nEnergy Density*: {5:.2f} RF/mB".format(len(blades), totalExp, idealExpansion, totalExp/idealExpansion,
        bladeMult, energyDensity), inline=False)
        results.set_footer(text="* Coil conductivity & Throughput bonus (overhaul) excluded! \n"
                                "Turbine Calculator Bot by FishingPole#3673")
        if ctx.channel.id in (752540645117132840, 708428479787434400):
            await ctx.send(embed=results)
    else:
        results = discord.Embed(title="Error in command!", colour=0xd50505, description="Oh no! The bot could not"
                                                                                      " calculate the turbine!")
        if len(error) > 1000:
            error = "{}... (too long)".format(error[:1000])
        results.add_field(name="Errors detected:", value="{}".format(error), inline=False)
        results.set_footer(text="Turbine Calculator Bot by FishingPole#3673")
        if ctx.channel.id in (752540645117132840, 708428479787434400):
            await ctx.send(embed=results)


@client.command(aliases=["resources"])
async def cost(ctx, *args):
    args, blades, bladeCounts = list(args), [], {alias: 0 for alias in list(bladeAliases)}
    bladesString, inputError, errorMsg, bearingDiameter, turbineDiameter, turbineString = "", False, "", 0, 0, ""

    # check for enough arguments
    try:

        # check for invalid turbine diameter
        try:
            turbineDiameter = int(args[0])
            if turbineDiameter < 3 or turbineDiameter > 24:
                inputError = True
                errorMsg += "Turbine diameter must be between 3 and 24 blocks!\n"
        except ValueError:
            inputError = True
            errorMsg += "Turbine diameter must be a number!\n"

        # check for invalid bearing diameter
        try:
            bearingDiameter = int(args[1])
            if bearingDiameter < 1 or bearingDiameter > turbineDiameter - 2 or bearingDiameter % 2 != turbineDiameter % 2:
                inputError = True
                errorMsg += "Bearing diameter must be between 1 and (turbine's diameter) -2, and mod(bearingDiameter, 2) " \
                            "must equal mod(turbineDiameter, 2)!\n"
        except ValueError:
            inputError = True
            errorMsg += "Bearing diameter must be a number!\n"

        # check for invalid input string
        turbineString = args[2]
        if turbineString[0] not in ("o", "u", "p"):
            inputError = True
            errorMsg += "Invalid calculation mode detected.\n"

        # check for invalid length
        if len(turbineString) > 25:
            inputError = True
            errorMsg += "Turbine is too long! (max length 24)\n"
        elif len(turbineString) < 2:
            inputError = True
            errorMsg += "Turbine is too short! (min length 1)\n"

        for i in range(1, len(turbineString)):
            bladeFound = False
            for bladeName, coded in bladeConversion.items():
                if turbineString[i] == coded:
                    blades.append(bladeName)
                    bladeFound = True
                    if bladeName not in ("stator", "steel", "sic", "extreme") and turbineString[0] in ("u", "p"):
                        inputError = True
                        errorMsg += "Blade at position {} doesn't exist in pre-overhaul!\n".format(i + 1)
                    break
            if not bladeFound:
                inputError = True
                errorMsg += "Invalid blade found at position {}.\n".format(i + 1)
    except IndexError:
        inputError = True
        errorMsg += "At least one argument is missing!\n"

    if not inputError:
        shaftLength = len(turbineString) - 1
        bearings = 2 * (bearingDiameter ** 2)
        frames = 8 * (turbineDiameter + 1) + 4 * shaftLength
        casings = 2 * (turbineDiameter ** 2) + 4 * (turbineDiameter * shaftLength) - 2 * bearings - 3
        shafts = (shaftLength * bearings) // 2
        rotorBlades = 2 * shaftLength * bearingDiameter * (turbineDiameter - bearingDiameter)

        for blade in blades:
            bladeCounts[blade] += (rotorBlades//shaftLength)

        results = discord.Embed(title="Turbine Blocks", colour=0x123456, description="A list of blocks needed to build the "
                                                                                     "turbine.")
        results.add_field(name="Turbine Dimensions:", value="Diameter: {0}\nBearing Diameter: {1}\nShaft Length: {2}\n"
                          .format(turbineDiameter, bearingDiameter, shaftLength))
        if turbineString[0] == "o":
            blocksString = "Casings (total): {4} ({0})^\nCasings (as frame): {1}\nBearings: {2}\nShafts: {3}\nCoils: {2}^^\n" \
                           "Inlets: 1\nOutlets: 1\nController: 1\n".format(casings, frames, bearings, shafts, casings+frames)
            blocksString += "^Turbine glass required for transparent turbine.\n^^Minimum coils needed for no penalty " \
                            "in coil efficiency."
        else:
            blocksString = "Casings: {0}\nFrames: {1}\nBearings: {2}\nShafts: {3}\nCoils: {2}^\n"\
                "Inlets: 1\nOutlets: 1\nController: 1\n".format(casings, frames, bearings, shafts)
            blocksString += "^Minimum coils needed for no penalty in coil efficiency."
        results.add_field(name="Blocks required:", value=blocksString, inline=False)

        bladesString += "Total blades: {}\n".format(rotorBlades)
        for rotorName, rotorCount in bladeCounts.items():
            if rotorCount == 0:
                continue
            bladesString += "{0} x{1}\n".format(client.get_emoji(bladeAliases[rotorName][-1]), rotorCount)

        results.add_field(name="Blades required:", value=bladesString)
        results.set_footer(text="Turbine Calculator Bot by FishingPole#3673")
        if ctx.channel.id in (752540645117132840, 708428479787434400):
            await ctx.send(embed=results)
    else:
        results = discord.Embed(title="Error in command!", colour=0xd50505, description="Oh no! The bot could not"
                                                                                        " calculate the turbine!")
        if len(errorMsg) > 1000:
            errorMsg = "{}... (too long)".format(errorMsg[:1000])
        results.add_field(name="Errors detected:", value="{}".format(errorMsg), inline=False)
        results.set_footer(text="Turbine Calculator Bot by FishingPole#3673")
        if ctx.channel.id in (752540645117132840, 708428479787434400):
            await ctx.send(embed=results)

client.run([REDACTED])

