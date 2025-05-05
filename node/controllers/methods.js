const asyncWrapper = require("../middleware/asyncwrapper"); 
const accountModel = require("../models/accounts.js")
const {OurErrorVersion} = require("../middleware/error.js")
const bcrypt = require("bcrypt")

module.exports = {
    createAccount: asyncWrapper(async(req, res) => {
        const { name, pin, id } = req.body;

        if (!name || !pin || !id) {
            throw new OurErrorVersion("Please provide all values", 400);
        }

        const new_pin = await bcrypt.hash(pin, 10)

        await accountModel.create({ name, id, pin: new_pin, balance: 0 });

        res.status(200).json({ account: {
            name,
            pin: new_pin,
            id,
            balance: 0
        }, msg: "Account created successfully", success:true });
    }),

    getAccount: asyncWrapper(async(req, res) => {
        const {ID, PIN: pin_plain} = req.body
        const {id, balance, name, pin_hash} = await accountModel.findOne({id: ID})

        console.log(name, id, balance, pin_hash, await bcrypt.compare(pin_plain, pin_hash))

        if(!name || !id || !balance || !pin_hash || !await bcrypt.compare(pin_plain, pin_hash)) {
            throw new OurErrorVersion(`Wallet ID ${ID} with PIN ${pin_plain} not found`, 404)
        }

        res.status(200).json({account: {id, balance, name}, msg: "Account get successful", success: true})
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