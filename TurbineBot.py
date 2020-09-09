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
                "une-90": ["une-90", "unwieldy-90", 752973096742289428],
                "une-192": ["une-192", "unwieldy-192", 752973096922644520],
                "une-231": ["une-231", "unwieldy-231", 752973096700608615],
                "edelstahl": ["edelstahl", "ultralight-edelstahl", "ul-edel", 752973096738226316],
                "niosteel": ["niosteel", "niobium-steel", "nios", 752973097044279437],
                "steel": ["steel", "ste", "s", 752974289766187068],
                "neptunium": ["neptunium", "np", 752973096884895866],
                "plutonium": ["plutonium", "pu", 752973097170239498],
                "legierung": ["legierung", "ultralight-legierung", "ul-legie", 752973096641888348],
                "extnio": ["extnio", "extremenio", "extreme-nio", "enio", 752973097040347167],
                "extreme": ["extreme", "ext", "ex", 752974289719918663],
                "americium": ["americium", "am", 752973096561934437],
                "curium": ["curium", "cm", 752973096608071770],
                "sicnio": ["sicnio", "sicniosic", 752973097300131890],
                "matrix": ["matrix", "ultralight-matrix", "ul-matrix", 752973096771780721],
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

steamAliases = {"hps": ["hps", "High Pressure Steam", "highpressuresteam", "high pressure steam", "hp steam"],
                "lps": ["lps", "Low Pressure Steam", "lowpressuresteam", "lp steam", "low pressure steam"],
                "steam": ["steam", "Steam", "mek steam", "tes", "forge steam", "te steam"], "scs": ["scs",
                "Supercritical Steam", "supercritical steam", "sc steam", "scsteam"], "scco2": ["scco2",
                "Supercritical Carbon Dioxide", "sc co2", "supercritical co2", "supercritical carbon dioxide"],
                "n2": ["n2", "Hot Nitrogen", "nitrogen", "hot nitrogen", "hot n2"], "co2": ["co2", "Hot Carbon Dioxide",
                "carbon dioxide", "hot co2", "hot carbon dioxide"], "he": ["he", "Hot Helium", "helium", "hot helium",
                "hot he"], "ar": ["ar", "Hot Argon", "argon", "hot argon", "hot ar"], "ne": ["ne", "Hot Neon", "neon",
                "hot neon", "hot ne"]}

client = commands.Bot(command_prefix="&")
client.remove_command("help")

@client.event
async def on_ready():
    print('Bot online as {0.user}'.format(client))


@client.command()
async def ping(ctx):
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
    helpEmbed.add_field(name="&ping", value="The infamous ping command. Returns ping (in ms) of the bot.", inline=False)
    helpEmbed.add_field(name="&help", value="Prints this message.", inline=False)
    await ctx.send(embed=helpEmbed)


@client.command(aliases=["turbine", "plan"])
async def calc(ctx, *args):  # args: (overhaul/underhaul) (RF density) (ideal expansion) (blades)
    actualExp, idealExp, emojiBlades = [], [], ""
    totalExp, bladeMult, statorCount, steamType, inputError, args = 1, 0, 0, None, False, list(args)
    error = ""

    def idealMult(ideal, actual):
        return min(ideal, actual)/max(ideal, actual)

    # checks if there's enough arguments
    if len(args) < 3:
        inputError = True
        error += "At least one argument is missing!\n"

    # checks calculation mode (1st argument)
    if args[0].lower() not in ("overhaul", "underhaul", "preoverhaul"):
        inputError = True
        error += "\"{}\" is not a valid calculation mode!\n".format(args[0])

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
            if steamType.lower() in aliases:
                steamType = aliases[0]
                steamFound = True
                break

        if not steamFound:
            inputError = True
            error += "Turbine fuel \"{}\" is invalid!\n".format(steamType)

        blades = args[2:]

    # checks for invalid blades
    for i1 in range(len(blades)):
        bladeFound = False

        for aliases in bladeAliases.values():
            if blades[i1].lower() in aliases:
                bladeFound = True
                blades[i1] = aliases[0]
                emojiBlades += "{} ".format(str(client.get_emoji(aliases[-1])))
                break

        if not bladeFound:
            inputError = True
            error += "Blade #{} ({}) is invalid!\n".format(i1 + 1, blades[i1])

    if len(blades) > 24:
        inputError = True
        error += "This turbine is too long!\n"

    if not inputError:
        turbineLength, mode = len(blades), args[0].lower()

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
            elif mode == "underhaul" or mode == "preoverhaul":
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
        results.add_field(name="Blade configuration:", value="{}".format(emojiBlades), inline=False)
        results.add_field(name="Fuel Stats:", value="Name: {}\nIdeal Expansion: {:.0%}\nBase Energy: {:.0f} RF/mB".format(
            steamType, idealExpansion, steamRFMB), inline=False)
        results.add_field(name="Turbine Stats:", value="Turbine Length: {0} \nTotal Expansion: {1:.2%} [{2:.2f} x {3:.2%}]\n"
        "Rotor Efficiency: {4:.2%}\nEnergy Density*: {5:.2f} RF/mB".format(len(blades), totalExp, idealExpansion, totalExp/idealExpansion,
        bladeMult, energyDensity), inline=False)
        results.set_footer(text="* Coil conductivity & Throughput bonus (overhaul) excluded! \nTurbine Planner by"
                                " FishingPole#3673")
        await ctx.send(embed=results)
    else:
        results = discord.Embed(title="Error in command!", colour=0xd50505, description="Oh no! The bot could not"
                                                                                      " calculate the turbine!")
        results.add_field(name="Errors detected:", value="{}".format(error), inline=False)
        await ctx.send(embed=results)

client.run([REDACTED])
