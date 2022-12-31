from nba_data_miner import compare

def test_teams():
    # A test to check that field goal, 3P, 2P and FT make rates
    # are equal to (made/attempted)*100.
    # Other metrics cannot be tested as the data is updated after
    # each game.
    
    # Collect implied make rates from df.
    df = compare.teams("BKN", "BOS")

    for i in [1,2]:
        FG_test = (df.iloc[13,i]/df.iloc[14,i])*100
        three_p_test = (df.iloc[16,i]/df.iloc[17,i])*100
        two_p_test = (df.iloc[22,i]/df.iloc[23,i])*100
        FT_test = (df.iloc[19,i]/df.iloc[20,i])*100

        # Test with assert
        assert(round(FG_test,1)-0.5 <= df.iloc[15,i] <= round(FG_test,1)+0.5),"Field goal % value is incorrect"
        assert(round(three_p_test,1)-0.5 <= df.iloc[18,i] <= round(three_p_test,1)+0.5),"Three point % value is incorrect"
        assert(round(two_p_test,1)-0.5 <= df.iloc[24,i] <= round(two_p_test,1)+0.5),"Two point % value is incorrect"
        assert(round(FT_test,1)-0.5 <= df.iloc[21,i] <= round(FT_test,1)+0.5),"Free throw % value is incorrect"
