function VoiceSpeak(text) {
    const textToSpeak = text;
    const zhCnLangs = speechSynthesis.getVoices().filter(x => x.lang === 'zh-CN');
    const microsoftKangkangLang = zhCnLangs.find(x => x.name === 'Microsoft Kangkang - Chinese (Simplified, PRC)');
    const hi = new window.SpeechSynthesisUtterance(textToSpeak);

    hi.rate = 1.5;      // 语速，从0.1-10，默认为1，2表示正常语速的两倍
    hi.pitch = 1;       // 说话的高音，从 0-2，默认为1
    hi.lang = 'zh-CN';  // 使用的语言，例如 zh-CN
    hi.voice = microsoftKangkangLang;

    window.speechSynthesis.speak(hi);
}

