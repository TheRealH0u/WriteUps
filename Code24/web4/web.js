const express = require("express");
const app = express();
const cors = require("cors");
const fs = require('fs');
const path = require('path');
const router = express.Router();
const cookieParser = require("cookie-parser");
const session = require('express-session');
const http = require('http');
const server = http.createServer(app);
const crypto = require("crypto");
const Joi = require("joi");
const axios = require('axios');
const url = require('url');
const passport = require("passport");
const LocalStrategy = require("passport-local");

// Constants for encryption
const ENCRYPTION_KEY = Buffer.from('2528300a57100f20c1dd178601c41406988446669d5e2021e737db53ee04515c', "hex");
const INITIALIZATION_VECTOR = Buffer.from("70043c465c6f5ff339582aad910fc501", "hex");

// Validation schemas
const userInfoSchema = Joi.object({
  'username': Joi.string().min(3).max(30).required(),
  'firstName': Joi.string().required(),
  'lastName': Joi.string().required(),
  'password': Joi.string().min(8),
  'info': Joi.string()
});
const targetInfoSchema = Joi.object({
  'name': Joi.string().min(3).max(30).required(),
  'clan': Joi.string().min(3).max(30).required(),
  'picture_url': Joi.string().uri({ 'scheme': [/https?/] }),
  'picture_path': Joi.string()
}).xor("picture_url", "picture_path");

// Session configuration
const sessionMiddleware = session({
  'secret': "1234567890abcdef",
  'resave': false,
  'saveUninitialized': true,
  'cookie': {
    'maxAge': 86400000, // One day
    'httpOnly': true,
    'secure': false,
    'sameSite': 'strict'
  }
});

// Sample user data
const userTemplate = Object.create(null);
userTemplate.firstName = "Alan";
userTemplate.lastName = "Schaefer";
userTemplate.password = "Passw0rd$";

global.users = {
  'a_schaefer': userTemplate
};

// Middleware setup
router.use(cookieParser());
router.use(express.urlencoded({ 'extended': true }));
router.use(express.json());
router.use(sessionMiddleware);
router.use(passport.authenticate("session"));

// Passport configuration
passport.use(new LocalStrategy({
  'usernameField': "user",
  'passwordField': "password"
}, (username, password, done) => {
  if (typeof users[username] !== "object") {
    return done(null, false, { 'message': "Incorrect username or password." });
  }
  if (users[username].password !== password) {
    return done(null, false, { 'message': "Incorrect username or password." });
  }
  return done(null, {
    'username': username,
    'firstName': users[username].firstName,
    'lastName': users[username].lastName
  });
}));

passport.serializeUser((user, done) => done(null, user));
passport.deserializeUser((user, done) => done(null, user));

// Routes
router.post("/login", passport.authenticate("local"), async (req, res) => {
  res.cookie("user", encryptCookie(JSON.stringify({
    'username': req.user.username,
    'firstName': req.user.firstName,
    'lastName': req.user.lastName
  })));
  res.status(200).json({
    'user': {
      'username': req.user.username,
      'firstName': req.user.firstName,
      'lastName': req.user.lastName
    }
  });
});

router.get("/loggedin", async (req, res) => {
  if (req.isAuthenticated()) {
    res.cookie("user", encryptCookie(JSON.stringify({
      'username': req.user.username,
      'firstName': req.user.firstName,
      'lastName': req.user.lastName
    })));
    res.status(200).json({
      'loggedin': true,
      'user': {
        'username': req.user.username,
        'firstName': req.user.firstName,
        'lastName': req.user.lastName
      }
    });
  } else {
    res.status(200).json({ 'loggedin': false });
  }
});

router.get("/get_targets", async (req, res) => {
  if (req.isAuthenticated()) {
    try {
      if (!req.cookies.user) {
        throw Error("User cookie not set!");
      }
      let responsePayload = { 'user': [], 'targets': [] };
      let decryptedCookie = decryptCookie(req.cookies.user);
      let validatedUser = validateObject(JSON.parse(decryptedCookie));
      let targetsData = JSON.parse(fs.readFileSync(path.join(__dirname, "files/targets.json")));
      for (let target of targetsData) {
        if (validateObject(target)) {
          responsePayload.targets.push(target);
        }
      }
      responsePayload.user.push(validatedUser);

      for (let key in responsePayload) {
        for (let item of responsePayload[key]) {
          if (item.picture_url) {
            axios.get(item.picture_url, { 'responseType': 'arraybuffer' })
              .then(response => {
                let fileName = url.parse(response.config.url).pathname.split('/').pop();
                let imageBuffer = Buffer.from(response.data, 'binary');
                fs.writeFileSync('pics/' + fileName, imageBuffer);
              })
              .catch(err => console.log(err));
          }
        }
      }

      res.status(200).json(responsePayload);
    } catch (error) {
      console.log(error);
      res.status(500).json({ 'msg': "Something went wrong." });
    }
  } else {
    res.status(401).json({ 'msg': "Not authenticated" });
  }
});

router.get("/include", (req, res) => {
  if (req.isAuthenticated()) {
    let filePath = path.join(__dirname, "files/" + req.query.p);
    if (filePath) {
      try {
        require(filePath);
        res.status(200).json({ 'msg': 'ok' });
      } catch (err) {
        res.status(500).json({ 'msg': "Something went wrong!" });
      }
    }
  } else {
    res.status(401).json({ 'msg': "Not authenticated" });
  }
});

router.post("/logout", (req, res, next) => {
  req.logout(err => {
    if (err) {
      console.log(err);
      return next(err);
    }
    res.status(200).json({ 'status': 'OK' });
  });
});

// Static file setup
router.use(express.static(__dirname + '/view/'));
router.use(express.static(__dirname + '/pics/'));

router.use((err, req, res, next) => {
  console.error(err.stack);
  res.redirect('/');
});

router.use((req, res) => {
  let clientIp = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
  console.log("Wrong URL entered: " + req.originalUrl + ". IP: " + clientIp);
  res.redirect('/');
});

// CORS configuration
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "http://pred-targets.codectf.localos.io");
  next();
});
app.use(router);
app.use(cors({ 'origin': ["http://pred-targets.codectf.localos.io"], 'credentials': true }));

// Start server
server.listen(3000, () => console.log("listening on *:3000"));

// Helper functions
const validateObject = object => {
  let userValidation = userInfoSchema.validate(object);
  let targetValidation = targetInfoSchema.validate(object);
  return userValidation.error ? !targetValidation.error && targetValidation.value : userValidation.value;
};

const encryptCookie = plaintext => {
  let cipher = crypto.createCipheriv("aes-256-cbc", ENCRYPTION_KEY, INITIALIZATION_VECTOR);
  return Buffer.from(cipher.update(plaintext, "utf8", "hex") + cipher.final('hex')).toString("base64");
};

const decryptCookie = encrypted => {
  let encryptedBuffer = Buffer.from(encrypted, "base64");
  let decipher = crypto.createDecipheriv("aes-256-cbc", ENCRYPTION_KEY, INITIALIZATION_VECTOR);
  return decipher.update(encryptedBuffer.toString("utf8"), "hex", "utf8") + decipher.final("utf8");
};
