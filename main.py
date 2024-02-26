import srcomapi, srcomapi.datatypes as dt
from texttable import Texttable
import urllib3


def main():

    api = srcomapi.SpeedrunCom(); api.debug = 0
    gameName = "borderlands 2"
    game = api.search(dt.Game, {"name": gameName})[0]
    tableCategories = Texttable()
    tableCategories.set_cols_dtype(['i','t'])
    categories = []
    tableCategories.add_rows([["Index","Speedrunning Categories"]])
    for eachCategory in range(len(game.categories)):
        tableCategories.add_row([eachCategory,str(game.categories[eachCategory])[11:-2]])
    # t.add_rows([["Current Categories"], (print(', ["' + category + ']"') for category in categories)])

    # t.add_rows(eachCategory))
    print("Please select a speedrunning category with input 0-" + str(len(game.categories)-1) + " and hit 'enter'")
    print(tableCategories.draw())
    # print(game)
    # print(game.categories)
    # print(game.categories[0].records[0].runs)
    # print(game.categories[0].records[0].runs[0]["run"].times)
    
    while True:
        try:
            chosenCat = int(input(""))
        except ValueError:
            print("Invalid input, please select a speedrunning category with input 0-" + str(len(game.categories)-1) + " and hit 'enter'")
            continue
        if chosenCat < 0 or chosenCat >= len(game.categories):
            print("Invalid input, please select a speedrunning category with input 0-" + str(len(game.categories)-1) + " and hit 'enter'")
            continue
        else:
            break
    print("You have selected: " + str(game.categories[chosenCat])[11:-2])
    print("Printing the data for the fastest " + str(game.categories[chosenCat])[11:-2] + " run:")

    # print(game.categories[chosenCat].records[0].runs)
    # print(len(game.categories[chosenCat].records[0].runs))

    # print(game.categories[chosenCat].records[0].runs[0]["run"].embeds)
    
    tableRuns = Texttable()
    tableRuns.set_cols_dtype(['t','t'])
    tableRuns.add_rows([["Variable","Values"]])
    tableRuns.add_row(['game',gameName])
    tableRuns.add_row(["category",str(game.categories[chosenCat])[11:-2]])
    # data = ['category', 'comment', 'data', 'date', 'embeds', 'endpoint', 'game', 'id', 'level', 'players', 'players', 'splits', 'status', 'submitted', 'system', 'times', 'values', 'videos', 'weblink']
    data = ['comment', 'date', 'endpoint', 'id', 'level', 'players', 'splits', 'status', 'submitted', 'system', 'times', 'values', 'videos', 'weblink']
    for eachData in data:
        # print("**" + eachData + ':     ' + str(getattr(game.categories[chosenCat].records[0].runs[0]["run"],eachData)))
        if eachData == "players":
            playerStr = ""
            for eachPlayer in range(len(getattr(game.categories[chosenCat].records[0].runs[0]["run"],eachData))):
                if eachPlayer != 0:
                    playerStr += ", "
                playerStr += str(getattr(game.categories[chosenCat].records[0].runs[0]["run"],eachData)[eachPlayer])[7:-2]
            tableRuns.add_row([eachData,playerStr])
        elif eachData == "status":
            if getattr(game.categories[chosenCat].records[0].runs[0]["run"],eachData)['status'] != 'verified':
                tableRuns.add_row([eachData,'status: ' + str(getattr(game.categories[chosenCat].records[0].runs[0]["run"],eachData)['status'])])
            else:
                statusStr = ""
                for k, v in getattr(game.categories[chosenCat].records[0].runs[0]["run"],eachData).items():
                    if str(k) == 'verify-date':
                        statusStr += str(k) + ": " + str(v).replace("T", " ").replace("Z", "") + '\n'
                    else:
                        statusStr += str(k) + ": " + str(v) + '\n'
            statusStr = statusStr[:-1]
            tableRuns.add_row([eachData,statusStr])
        elif eachData == "submitted":
            tableRuns.add_row([eachData,'status: ' + str(getattr(game.categories[chosenCat].records[0].runs[0]["run"],eachData)).replace("T", " ").replace("Z", "")])
        elif eachData == "system":
            systemStr = ""
            for k, v in getattr(game.categories[chosenCat].records[0].runs[0]["run"],eachData).items():
                systemStr += str(k) + ": " + str(v) + '\n'
            systemStr = systemStr[:-1]
            tableRuns.add_row([eachData,systemStr])
        elif eachData == "times":
            timesStr = ""
            for k, v in getattr(game.categories[chosenCat].records[0].runs[0]["run"],eachData).items():
                if str(k)[-2:] != "_t":
                    if str(v)[0:2] == "PT":
                        timesStr += str(k) + ": " + str(v)[2:].replace("H","H ").replace("M","M ") + '\n'
                    else:
                        timesStr += str(k) + ": " + str(v) + '\n'
            timesStr = timesStr[:-1]
            tableRuns.add_row([eachData,timesStr])
        elif eachData == "videos":
            videosStr = ""
            for links, uri in getattr(game.categories[chosenCat].records[0].runs[0]["run"],eachData).items():
                videosStr += str(uri)[10:-3] + ', '
            videosStr = videosStr[:-2]
            tableRuns.add_row([eachData,videosStr])
        else:
            tableRuns.add_row([eachData,str(getattr(game.categories[chosenCat].records[0].runs[0]["run"],eachData))])
    print(tableRuns.draw())
    # sms_runs = {}
    # for category in game.categories:
    #     if not category.name in sms_runs:
    #         sms_runs[category.name] = {}
    #     if category.type == 'per-level':
    #         for level in game.levels:
    #             sms_runs[category.name][level.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/level/{}/{}?embed=variables".format(game.id, level.id, category.id)))
    #     else:
    #         sms_runs[category.name] = dt.Leaderboard(api, data=api.get("leaderboards/{}/category/{}?embed=variables".format(game.id, category.id)))
    # print(sms_runs['Any% w/DLC'])

    print("Done.")
    """
    print('\n\n\n')

    # resp = urllib3.request("GET", "http://www.speedrun.com/api/v1/leaderboards/bl2/records?top=1")
    # print(resp.status)
    # print(resp.data)

    game = api.search(dt.Game, {"name": "mc"})[0]
    print(game.categories)
    data = ['category', 'comment', 'data', 'date', 'embeds', 'endpoint', 'game', 'id', 'level', 'players', 'players', 'splits', 'status', 'submitted', 'system', 'times', 'values', 'videos', 'weblink']
    # for eachData in data:
    #     print("**" + eachData + ':     ' + str(getattr(game.categories[3].records[0].runs[0]["run"],eachData)))
    print('******splits:     ' + str(game.categories[3].records[0].runs[0]["run"].splits))
    """
if __name__ == "__main__":
    main()
