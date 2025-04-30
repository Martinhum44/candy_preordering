const aMONGOOSE = require("mongoose")

const accountModel = new aMONGOOSE.Schema({
    name:{
        type: String,
        required: [true, "Name was not provided"],
        maxlength: [50, "Name cannot be greater than 50 characters"]
    },
    id:{
        type: String,
        required: [true, "Id was not provided"],
    },
    pin:{
        type: String,
        minlength: [4, "PIN must be 4 characters"],
        maxlength: [4, "PIN must be 4 characters"],
        required: [true, "PIN was not provided"],
    },
    balance:{
        type: Number,
        default: 0
    },
})

module.exports = aMONGOOSE.model("User",accountModel)