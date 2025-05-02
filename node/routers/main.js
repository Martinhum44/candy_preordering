const express = require("express")
const router = express.Router()
const cors = require("cors")
const { createAccount, getAccount, searchAccount, chargeAccount, deleteAccount, payAccount } = require("../controllers/methods")

router.use(express.json())
router.use(cors())

router.get("/get-account/:ID/:PIN", getAccount)
router.post("/create-account", createAccount)
router.get("/search-account", searchAccount)
router.patch("/charge-account/:ID", chargeAccount)
router.delete("/delete-account/:ID", deleteAccount)
router.patch("/pay-account/:ID", payAccount)

module.exports = router