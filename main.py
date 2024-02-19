import srcomapi, srcomapi.datatypes as dt
from texttable import Texttable
import urllib3


def main():

    api = srcomapi.SpeedrunCom(); api.debug = 0

    game = api.search(dt.Game, {"name": "borderlands 2"})[0]
    table = Texttable()
    table.set_cols_dtype(['i','t'])
    categories = []
    table.add_rows([["Index","Current Categories"]])
    for eachCategory in range(len(game.categories)):
        table.add_row([eachCategory,str(game.categories[eachCategory])[11:-2]])
    # t.add_rows([["Current Categories"], (print(', ["' + category + ']"') for category in categories)])

    # t.add_rows(eachCategory))
    print("Please select a speedrunning category with input 0-" + str(len(game.categories)) + "and hit 'enter'")
    print(table.draw())
    # print(game)
    # print(game.categories)
    # print(game.categories[0].records[0].runs)
    # print(game.categories[0].records[0].runs[0]["run"].times)
    
    while True:
        try:
            chosenCat = int(input(""))
        except ValueError:
            print("Invalid input, please select a speedrunning category with input 0-" + str(len(game.categories)) + "and hit 'enter'")
            continue
        if chosenCat < 0 or chosenCat >= len(game.categories):
            print("Invalid input, please select a speedrunning category with input 0-" + str(len(game.categories)) + "and hit 'enter'")
            continue
        else:
            break
    print("You have selected: " + str(game.categories[chosenCat])[11:-2])

    print(game.categories[chosenCat].records[0].runs)
    print(len(game.categories[chosenCat].records[0].runs))

    print(game.categories[chosenCat].records[0].runs[0]["run"].embeds)
    

    data = ['category', 'comment', 'data', 'date', 'embeds', 'endpoint', 'game', 'id', 'level', 'players', 'players', 'splits', 'status', 'submitted', 'system', 'times', 'values', 'videos', 'weblink']
    for eachData in data:
        print("**" + eachData + ':     ' + str(getattr(game.categories[chosenCat].records[0].runs[0]["run"],eachData)))
    
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
