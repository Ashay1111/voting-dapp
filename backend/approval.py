from pyteal import *

def approval():
    creator = Global.creator_address()
    vote_option = Bytes("vote_option")
    voted = Bytes("voted")

    on_create = Seq([
        App.globalPut(Bytes("OptionA"), Int(0)),
        App.globalPut(Bytes("OptionB"), Int(0)),
        Return(Int(1))
    ])

    already_voted = App.localGetEx(Int(0), App.id(), voted)

    vote = Seq([
        already_voted,
        If(already_voted.hasValue()).Then(
            Return(Int(0))
        ),
        App.localPut(Int(0), voted, Int(1)),
        If(Txn.application_args[0] == Bytes("voteA")).Then(
            App.globalPut(Bytes("OptionA"), App.globalGet(Bytes("OptionA")) + Int(1))
        ).ElseIf(Txn.application_args[0] == Bytes("voteB")).Then(
            App.globalPut(Bytes("OptionB"), App.globalGet(Bytes("OptionB")) + Int(1))
        ),
        Return(Int(1))
    ])

    handle_noop = Cond(
        [Txn.application_args[0] == Bytes("voteA"), vote],
        [Txn.application_args[0] == Bytes("voteB"), vote]
    )

    program = Cond(
        [Txn.application_id() == Int(0), on_create],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )

    return program

if __name__ == "__main__":
    print(compileTeal(approval(), mode=Mode.Application))
