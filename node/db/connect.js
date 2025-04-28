const MONGOOSE = require("mongoose")

async function connect(url) {
    return MONGOOSE.connect(url,{
        useNewUrlParser:true,
        useUnifiedTopology:true
    })
}
  
module.exports = connect