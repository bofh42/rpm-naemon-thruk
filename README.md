# naemon-thruk-rpms
These are my rpm spec files for [Naemon](https://www.naemon.io/), [Thruk](https://thruk.org/) and other playing parts to do monitoring.

# Description
Here are Monitoring rpm spec files for [Naemon](https://www.naemon.io/) / [Thruk](https://thruk.org/) and all that i use around them.  
Build and tested for/with [Red Hat Enterprise Linux Server](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux/server) 9
or clones like [AlmaLinux](https://almalinux.org/), [Rocky Linux](https://rockylinux.org/).  
It is based on the spec files from [home:naemon - openSUSE Build Service](https://build.opensuse.org/project/show/home:naemon).  
My goal is to build all with only spec files and get sources from git repos.

# Build rpms
You can build rpms from just the spec file with `spectool -gf -R <spec>` and `rpmbuild -bb <spec>`.

# Full build cycle
The order of building it matters, because of some BuildRequires.  
For me it looks like this:
```
for i in naemon naemon-core naemon-livestatus naemon-vimvault \
         gearmand mod_gearman libthruk thruk-selinux thruk ; do
  run-image.sh -o el9 -- ~/build/bin/rbba --source rpmbuild/specs/${i}.spec || break
done
```
But my rbba does lots of things for every spec file in a special prepared container
- `createrepo` for `%{_rpmdir}` and `%{_srcrpmdir}`
- setup a local `/etc/yum.repos.d/rpmbuild.repo` pointing there
- `spectool -gf -R <spec>`
- `sudo yum-builddep -y <spec>`
- `rpmbuild -ba <spec>`
```
