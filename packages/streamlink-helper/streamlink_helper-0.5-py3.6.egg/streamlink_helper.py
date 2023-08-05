from configuration import Configuration
from util import followscraper, execute_streamlink_command


def main():
    streamlink_helper = StreamlinkHelper()


class StreamlinkHelper:
    def __init__(self):
        configuration = Configuration()
        if not configuration.user_id:
            return
        currently_online = followscraper(configuration.user_id)
        print("\nThese streamers that you follow are currently online:\n")
        i = 0
        selection_list = []
        for name, url in currently_online.items():
            try:
                print("({}) {}".format(i, name))
            except UnicodeEncodeError:
                print("({}) {} \n".format(i, name.encode('utf-8')))
            selection_list.append(url)
            i += 1
        try:
            # TODO: Randomization when no number selected
            number_selection = int(input("Choose a number and press enter to select stream: "))
            selected_stream = selection_list[number_selection]
            execute_streamlink_command(selected_stream, configuration)
        except ValueError:
            print("Please enter a number.")
        except IndexError:
            print("Please enter a number on the list.")

main()