from results_service import ResultStore

class ResultsController:

    def __init__(self) -> None:
        self.store: ResultStore = ResultStore()
    
    def get_result(self, id: int) -> dict:
        return self.store.get_result(id)
    
    def new_result(self, result: dict) -> dict:
        self.store.new_result(result)
        return {}
    
    def reset(self) -> None:
        self.store.reset()
    
    def scoreboard(self) -> dict:
        
        def fill_entry_list(scoreboard):
            for constituency in self.store.store:
                for party_details in constituency["partyResults"]:
                    if party_details["party"] not in scoreboard.keys():
                        scoreboard[party_details["party"]] = {"seats": 0, "votes": 0, "vote_share": 0}          
        scoreboard = {}
        
        def get_const_winner(list_of_parties):
            winner = ''
            votes = -1
            
            for party in list_of_parties:
                if party['votes'] > votes:
                    votes = party['votes']
                    winner = party['party']                   
            return winner
            
        def fill_seats(scoreboard):
            for constituency in self.store.store:
                # winning_party = constituency["partyResults"][0]["party"]
                winning_party = get_const_winner(constituency["partyResults"])
                scoreboard[winning_party]["seats"] += 1
        
        def fill_votes(scoreboard):
            total_votes = 0
            for constituency in self.store.store:
                for party_details in constituency["partyResults"]:
                    party = party_details["party"]
                    no_of_votes = party_details["votes"]
                    scoreboard[party]["votes"] += no_of_votes
                    total_votes += no_of_votes
            for party in scoreboard.keys():
                scoreboard[party]["vote_share"] = '{:.1%}'.format((scoreboard[party]["votes"]/total_votes))
            
        def get_winner(scoreboard):
            for party in scoreboard.keys():
                if scoreboard[party]['seats'] >= 325:
                    return party
            return None
            
        fill_entry_list(scoreboard)
        fill_seats(scoreboard)
        fill_votes(scoreboard)
        winner = get_winner(scoreboard)
        scoreboard = {'winner': winner, 'parties': scoreboard}
        return scoreboard
