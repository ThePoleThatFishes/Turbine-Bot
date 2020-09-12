import discord
from discord.ext import commands
from math import pow, sqrt
from math import log as ln
import asyncio

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

overhaulAliases = ["overhaul", "oh", "nco", "over"]
preoverhaulAliases = ["pre-overhaul", "po", "underhaul", "preoverhaul", "uh", "nc"]

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
    "`&calc [mode] [fuel type] (dimensions) [blades]` or \n"
    "`&calc [mode] [RF/mB of fuel] [ideal expansion] (dimensions) [blades]`\n"
    "`mode`: Calculation mode. Can be overhaul or underhaul or preoverhaul (underhaul and preoverhaul are the same)\n"
    "`fuel type`: The type of gas that enters the turbine. See list of aliases for valid names. \n"
    "`RF/mB of fuel`: Base energy density of gas (**__not compatible with fuel type__**)\n "
    "`ideal expansion`: The ideal expansion of the gas. Must be input as a number (eg. 400% = 4) (**__not compatible with fuel type__**) \n"
    "`dimensions`: Optional parameter. Say `txby`, where x is turbine diameter and y is bearing diameter."
    "`blades`: The blades used in the turbine. See list of aliases for valid names.\n"
    "Order of arguments matters, capitalization doesn't matter, multi-word inputs are allowed but use quotes `\"high pressure steam\"`\n"
    "[List of Aliases]({})".format("https://github.com/ThePoleThatFishes/Turbine-Bot/blob/master/aliases.txt"), inline=False)
    helpEmbed.add_field(name="&ping", value="The infamous ping command. Returns ping (in ms) of the bot.", inline=False)
    helpEmbed.add_field(name="&help", value="Prints this message.", inline=False)
    helpEmbed.set_footer(text="Turbine Calculator Bot by FishingPole#3673")
    if ctx.channel.id in (752540645117132840, 708428479787434400):
        await ctx.send(embed=helpEmbed)

@client.command(aliases=["turbine", "plan"])
async def calc(ctx, *args):  # args: (overhaul/underhaul) (RF density) (ideal expansion) (blades)
    actualExp, idealExp, blades, emojiBlades = [], [], [], ""
    totalExp, bladeMult, statorCount, steamType, inputError, args = 1, 0, 0, None, False, list(args)
    error, blocksString, turbineStats, turbineDim, bearingDim, dimsInput, bladesString = "", "", "", 3, 1, False, ""
    bladeCounts = {alias: 0 for alias in list(bladeAliases)}
    minStatorExp, minBladeExp = 1, 2**1024

    def idealMult(ideal, actual):
        return min(ideal, actual)/max(ideal, actual)

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
                typeDetection = float(args[2])
                if typeDetection <= 0.0:
                    inputError = True
                    error += "Turbine fuel must have a positive expansion coefficient!\n"
            except ValueError:
                inputError = True
                error += "Missing expansion coefficient parameter!\n"

            # checks if turbine dimensions have been entered
            try:
                turbineDetect = int(args[3][1])
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
                            error += "Bearing diameter must be between 1 and Turbine diameter - 2, and" \
                                     " mod(TurbineDim, 2) == mod(BearingDim, 2)!\n"
                        else:
                            dimsInput = True
                            blades = args[4:]
                    except ValueError:
                        inputError = True
                        error += "Invalid bearing dimension!"
                except IndexError:
                    inputError = True
                    error += "Turbine dimensions \"{}\" are invalid!"

            except ValueError:
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
            steamType = args[1]

            for aliases in steamAliases.values():
                if (steamType.lower()).replace(" ", "") in aliases:
                    steamType = aliases[0]
                    steamFound = True
                    break

            if steamFound and (args[0] in preoverhaulAliases
                               and steamType not in ("hps", "lps", "steam")):
                inputError = True
                error += "Turbine fuel \"{}\" can't be used in {}!\n".format(steamType, args[0])

            if not steamFound:
                inputError = True
                error += "Turbine fuel \"{}\" is invalid!\n".format(steamType)

            # checks for dimensions
            try:
                turbineDetect = int(args[2][1])
                try:
                    bearingDetect = (args[2].lower()).index("b")
                    turbineDim = int(args[2][1:bearingDetect])
                    if not(3 <= turbineDim <= 24):
                        inputError = True
                        error += "Turbine diameter must be between 3 and 24 blocks!\n"
                    try:
                        bearingDim = int(args[2][bearingDetect + 1:])
                        if not(1 <= bearingDim <= turbineDim - 2 and turbineDim % 2 == bearingDim % 2):
                            inputError = True
                            error += "Bearing diameter must be between 1 and Turbine diameter - 2, and" \
                                     " mod(TurbineDim, 2) == mod(BearingDim, 2)!\n"
                        else:
                            dimsInput = True
                            blades = args[3:]
                    except ValueError:
                        inputError = True
                        error += "Invalid bearing dimension!"
                except IndexError:
                    inputError = True
                    error += "Turbine dimensions \"{}\" are invalid!"

            except ValueError:
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
                    emojiBlades += "{} ".format(str(client.get_emoji(aliases[-1])))
                    bladeCounts[blades[i1]] += 1
                    break

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

            if mode in overhaulAliases:
                actualExp.append(prevExp*sqrt(bladeStats[blades[i]][0]))
            elif mode in preoverhaulAliases:
                actualExp.append((prevExp + totalExp)/2)
                if blades[i] == "sic":
                    bladeMult += 0.05*idealMult(idealExp[i], actualExp[i])
            bladeMult += bladeStats[blades[i]][1]*idealMult(idealExp[i], actualExp[i])
            if bladeStats[blades[i]][2]:
                minStatorExp = min(minStatorExp, bladeStats[blades[i]][0])
                statorCount += 1
            else:
                minBladeExp = min(minBladeExp, bladeStats[blades[i]][0])

        bladeMult /= turbineLength - statorCount
        energyDensity = bladeMult * steamRFMB * idealMult(idealExpansion, totalExp)
        if steamType != "Custom":
            steamType = steamAliases[steamType][1]

        results = discord.Embed(title="{} Turbine".format(mode.capitalize()), colour=0x123456,
                                description="Stats of the given turbine:")
        results.add_field(name="Blade configuration:", value="{0}".format(emojiBlades), inline=False)
        results.add_field(name="Fuel Stats:", value="Name: {}\nBase Energy: {:.0f} RF/mB\nIdeal Expansion: {:.0%}".format(
            steamType, steamRFMB, idealExpansion), inline=False)

        if dimsInput:
            shaftLength = len(blades)
            bearings = 2 * (bearingDim ** 2)
            frames = 8 * (turbineDim + 1) + 4 * shaftLength
            casings = 2 * (turbineDim ** 2) + 4 * (turbineDim * shaftLength) - 2 * bearings - 3
            coils = min(bearings, 2 * turbineDim ** 2 - bearings - 2)
            if bearings > turbineDim ** 2:
                casings = 4 * (turbineDim * shaftLength) - 1
            shafts = (shaftLength * bearings) // 2
            rotorBlades = 2 * shaftLength * bearingDim * (turbineDim - bearingDim)
            coilPenalty = coils / bearings  # shows penalty for not enough coils
            bladesString += "Total blades: {}\n".format(rotorBlades)
            maxInput = (rotorBlades - statorCount * (rotorBlades//shaftLength))*100

            # Throughput Bonus calcs
            if minBladeExp <= 1.0:
                effMaxLen = 24.0
            elif minStatorExp >= 1.0:
                effMaxLen = max(1.0, min(24.0, ln(idealExpansion)/ln(minBladeExp)))
            else:
                effMaxLen = max(1.0, min(24.0, ln(idealExpansion) - 24*ln(minStatorExp)/(ln(minBladeExp)-ln(minStatorExp))))

            lengthBonus = maxInput/(100.0*effMaxLen*(rotorBlades//shaftLength))
            areaBonus = sqrt(2.0*maxInput/(100.0*shaftLength*24.0*effMaxLen))
            throughputBonus = 1 + pow(lengthBonus*areaBonus, 2.0/3.0)
            newEnergyDensity = energyDensity*throughputBonus
            powerGen = int(newEnergyDensity*maxInput)

            for bladeName, bladeCount in bladeCounts.items():
                if bladeCount == 0:
                    continue
                else:
                    bladeCount *= rotorBlades // shaftLength
                    bladesString += "{0} x{1}\n".format(client.get_emoji(bladeAliases[bladeName][-1]), bladeCount)

            if mode in overhaulAliases:
                blocksString = "Casings (total): {4} ({0})*\nCasings (as frame): {1}\nBearings: {2}\nShafts: {3}\nCoils: {5}\n" \
                               "Inlets: 1\nOutlets: 1\nController: 1\nCoil Sparsity Penalty: {6:.2f}\**\n".format(casings, frames,
                                                                                                  bearings, shafts,
                                                                                                  casings + frames,
                                                                                                  coils, coilPenalty)

                turbineStats = "Dimensions: {0}x{0}x{1} ({2}x{2} Bearing)\nTotal Expansion: {3:.2%} [{4:.2f} x {5:.2%}]" \
                                "\nRotor Efficiency: {6:.2%}\nEnergy Density\*: {7:.2f} RF/mB\nMax Input: {8:,} mB/t\n" \
                                "Power output\*: {9:,} RF/t\nThroughput Bonus: {10:.2%}".format(turbineDim, len(blades),
                                                                                              bearingDim, totalExp, idealExpansion,
                                                                                              totalExp/idealExpansion, bladeMult,
                                                                                              newEnergyDensity, maxInput, powerGen, throughputBonus)
                results.set_footer(text="*Coil efficiency is excluded.\n"
                                        "Turbine Bot by FishingPole#3673")
                footer = "*Turbine glass required for a transparent turbine\n" \
                            "**Multiplier applied to coil efficiency when the coils are fewer than the bearings.\n" \
                            "Turbine Bot by FishingPole#3673"

            elif mode in preoverhaulAliases:
                blocksString = "Casings: {0}\nFrames: {1}\nBearings: {2}\nShafts: {3}\nCoils: {4}\n" \
                               "Inlets: 1\nOutlets: 1\nController: 1\nCoil Sparsity Penalty*: {5:.2f}\n".format(casings, frames,
                                                                                                  bearings, shafts,
                                                                                                  coils, coilPenalty)

                turbineStats = "Dimensions: {0}x{0}x{1} ({2}x{2} Bearing)\nTotal Expansion: {3:.2%} [{4:.2f} x {5:.2%}]" \
                               "\nRotor Efficiency: {6:.2%}\nEnergy Density\*: {7:.2f} RF/mB\nMax Input: {8:,} mB/t\n" \
                               "Power output\*: {9:,} RF/t".format(turbineDim, len(blades), bearingDim, totalExp, idealExpansion,
                                                                 totalExp/idealExpansion, bladeMult, energyDensity, maxInput
                                                                 , int(maxInput*energyDensity))
                results.set_footer(text="*Coil efficiency is excluded.\n"        
                                        "Turbine Bot by FishingPole#3673")
                footer = "*Multiplier applied to coil efficiency when the coils are fewer than the bearings.\n" \
                         "Turbine Bot by FishingPole#3673"

            resources = discord.Embed(title="{} Turbine Blocks List".format(mode.capitalize()), colour=0x123456,
                                      description="A list of blocks needed to construct the turbine.")
            resources.add_field(name="Blocks Required:", value=blocksString, inline=False)
            resources.add_field(name="Blades Required:", value=bladesString, inline=False)
            resources.set_footer(text=footer)
        else:
            turbineStats = "Shaft Length: {0}\nTotal Expansion: {1:.2%} [{2:.2f} x {3:.2%}]\nRotor Efficiency: {4:.2%}\n" \
                           "Energy Density:\* {5:.2f} RF/mB".format(len(blades), totalExp, idealExpansion,
                                                                    totalExp/idealExpansion, bladeMult, energyDensity)
            results.set_footer(text="*Coil conductivity & throughput bonus excluded!\nTurbine Bot by FishingPole#3673")

        results.add_field(name="Turbine Stats:", value=turbineStats, inline=False)

        if ctx.channel.id in (752540645117132840, 708428479787434400):
            if dimsInput:
                botMessage = await ctx.send(embed=results)
                await botMessage.add_reaction("\U000025C0")
                await botMessage.add_reaction("\U000025B6")
                await botMessage.add_reaction("\U000023F9")

                def check(r, u):
                    return u == ctx.message.author and str(r.emoji) in ("\U000025B6", "\U000025C0", "\U000023F9")

                while True:
                    try:
                        reaction, user = await client.wait_for("reaction_add", timeout=60.0, check=check)
                    except asyncio.TimeoutError:
                        await botMessage.clear_reactions()
                        break
                    else:
                        if str(reaction.emoji) == "\U000025B6":
                            await botMessage.edit(embed=resources)
                            await botMessage.remove_reaction(emoji="\U000025B6", member=user)
                        elif str(reaction.emoji) == "\U000025C0":
                            await botMessage.edit(embed=results)
                            await botMessage.remove_reaction(emoji="\U000025C0", member=user)
                        elif str(reaction.emoji) == "\U000023F9":
                            await botMessage.clear_reactions()
                            break

            else:
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


client.run([REDACTED])

