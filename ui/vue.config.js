module.exports = {
    chainWebpack: config => {
        config.plugin('copy')
            .tap(([pathConfigs]) => {
                const to = pathConfigs[0].to + '/icons';
                pathConfigs[0].force = true;
                pathConfigs.unshift({
                    from: '../icons/resources',
                    to,
                });
                return [pathConfigs];
            });
    }
};
