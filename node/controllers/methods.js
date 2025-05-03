const asyncWrapper = require("../middleware/asyncwrapper"); 
const accountModel = require("../models/accounts.js")
const {OurErrorVersion} = require("../middleware/error.js")

module.exports = {
    createAccount: asyncWrapper(async(req, res) => {
        const { name, pin, id } = req.body;

        if (!name || !pin || !id) {
            throw new OurErrorVersion("Please provide all values", 400);
        }

        await accountModel.create({ name, pin, id, balance: 0 });

        res.status(200).json({ account: {
            name,
            pin,
            id,
            balance: 0
        }, msg: "Account created successfully", success:true });
    }),

    getAccount: asyncWrapper(async(req, res) => {
        const {ID, PIN} = req.params
        const acc = await accountModel.findOne({id: ID, pin: PIN})

        if(!acc) {
            throw new OurErrorVersion(`Wallet ID ${ID} with PIN ${PIN} not found`, 404)
        }

        res.status(200).json({account: acc, msg: "Account get successful", success: true})
    }),

    searchAccount: asyncWrapper((req, res) => {
        res.status(200).json({ msg: "created account", success:true });
    }),

    chargeAccount: asyncWrapper((req, res) => {
        res.status(200).json({ msg: "charged account", success:true });
    }),

    deleteAccount: asyncWrapper((req, res) => {
        res.status(200).json({ msg: "deleted account", success:true });
    }),

    payAccount: asyncWrapper((req, res) => {
        res.status(200).json({ msg: "paid account", success:true });
    }),
}